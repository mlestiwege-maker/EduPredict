import json, sys
from pathlib import Path
import numpy as np, pandas as pd
from sklearn.model_selection import GroupShuffleSplit
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, brier_score_loss
import joblib, warnings
warnings.filterwarnings('ignore')
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'ml/data/sample/buse'; MODELS=ROOT/'ml/models'; REPORTS=ROOT/'ml/reports'
MODELS.mkdir(parents=True, exist_ok=True); REPORTS.mkdir(parents=True, exist_ok=True)
CHECKPOINT_FEATURES={'week_0':['previous_gpa','admission_score','year_of_study','credit_load'],'week_4':['previous_gpa','admission_score','year_of_study','credit_load','attendance_rate_w4','assessment_avg_w4','lms_logins_w4','lms_resources_w4'],'week_8':['previous_gpa','admission_score','year_of_study','credit_load','attendance_rate_w8','assessment_avg_w8','lms_logins_w8','lms_resources_w8','late_submissions'],'week_12':['previous_gpa','admission_score','year_of_study','credit_load','attendance_rate_w12','assessment_avg_w12','lms_logins_w12','lms_resources_w12','late_submissions','time_on_task']}

def load_frame():
    np.random.seed(42)
    stu=pd.read_csv(DATA/'students.csv'); enr=pd.read_csv(DATA/'enrolments.csv'); att=pd.read_csv(DATA/'attendance.csv'); asm=pd.read_csv(DATA/'assessments.csv'); lms=pd.read_csv(DATA/'lms_activity.csv'); out=pd.read_csv(DATA/'outcomes_training.csv')
    df=out.merge(stu,on='student_pseudonym',how='left').merge(enr,on=['student_pseudonym','course_code','period_code'],how='left').merge(att,on=['student_pseudonym','course_code','period_code'],how='left')
    asm_agg=asm.groupby(['student_pseudonym','course_code','period_code']).agg(assessment_avg=('score','mean'),late_submissions=('is_late','sum')).reset_index()
    df=df.merge(asm_agg,on=['student_pseudonym','course_code','period_code'],how='left').merge(lms,on=['student_pseudonym','course_code','period_code'],how='left')
    for w,f in [('4',0.9),('8',0.95),('12',1.0)]:
        df[f'attendance_rate_w{w}']=(df['attendance_rate']*np.random.uniform(0.85,f,len(df))).clip(0,100)
        df[f'assessment_avg_w{w}']=(df['assessment_avg']*np.random.uniform(0.8,f,len(df))).clip(0,100)
        df[f'lms_logins_w{w}']=(df['logins_count']*float(w)/12*np.random.uniform(0.8,1.1,len(df))).clip(0)
        df[f'lms_resources_w{w}']=(df['resources_accessed']*float(w)/12*np.random.uniform(0.8,1.1,len(df))).clip(0)
    df['time_on_task']=df['time_on_task_minutes']; df['target_at_risk']=(df['passed']==0).astype(int)
    return df.fillna(0)

def models():
    return {'Logistic Regression':LogisticRegression(max_iter=600,class_weight='balanced',random_state=42),'Decision Tree':DecisionTreeClassifier(max_depth=6,min_samples_leaf=10,class_weight='balanced',random_state=42),'Random Forest':RandomForestClassifier(n_estimators=120,max_depth=8,min_samples_leaf=5,class_weight='balanced',random_state=42,n_jobs=2),'SVM':SVC(probability=True,class_weight='balanced',random_state=42),'Gradient Boosting':GradientBoostingClassifier(random_state=42),'MLP':MLPClassifier(hidden_layer_sizes=(32,16),max_iter=350,random_state=42)}

def train(checkpoint='week_4'):
    df=load_frame(); feats=CHECKPOINT_FEATURES.get(checkpoint,CHECKPOINT_FEATURES['week_4'])
    X=df[feats].astype(float); y=df['target_at_risk'].astype(int); g=df['student_pseudonym']
    tr,te=next(GroupShuffleSplit(n_splits=1,test_size=0.25,random_state=42).split(X,y,g))
    Xtr,Xte,ytr,yte=X.iloc[tr],X.iloc[te],y.iloc[tr],y.iloc[te]
    results=[]; best=(None,None,-1,None)
    for name,clf in models().items():
        pipe=Pipeline([('scaler',StandardScaler()),('clf',clf)]); pipe.fit(Xtr,ytr)
        proba=pipe.predict_proba(Xte)[:,1]; pred=(proba>=0.45).astype(int)
        m=dict(model=name,accuracy=round(float(accuracy_score(yte,pred)),4),precision=round(float(precision_score(yte,pred,zero_division=0)),4),recall=round(float(recall_score(yte,pred,zero_division=0)),4),f1=round(float(f1_score(yte,pred,zero_division=0)),4),roc_auc=round(float(roc_auc_score(yte,proba)),4) if len(np.unique(yte))>1 else 0.0,brier=round(float(brier_score_loss(yte,proba)),4),confusion=confusion_matrix(yte,pred).tolist())
        score=m['recall']*0.45+m['f1']*0.35+m['roc_auc']*0.2
        results.append(m);
        if score>best[2]: best=(name,pipe,score,m)
    sel_name,sel_pipe,_,sel_m=best; version=f'edupredict-{checkpoint}-v1'
    joblib.dump({'pipeline':sel_pipe,'features':feats,'checkpoint':checkpoint,'version':version,'model_name':sel_name}, MODELS/f'{version}.joblib')
    report={'status':'ok','dataset':'synthetic_buse_demo','institution_target':'Bindura University of Science Education (BUSE)','checkpoint':checkpoint,'target':'at_risk (passed==0 or risk factors)','n_records':int(len(df)),'n_test':int(len(yte)),'features':feats,'selected_model':sel_name,'selection':'0.45*recall+0.35*f1+0.2*roc_auc','selected_metrics':sel_m,'results':sorted(results,key=lambda x:x['f1'],reverse=True),'disclaimer':'Synthetic demo results only. Not real BUSE outcomes. Validate on approved institutional data with temporal holdout, no leakage, calibration, and fairness checks.'}
    (REPORTS/f'{version}.json').write_text(json.dumps(report,indent=2)); return report

def predict(checkpoint='week_4'):
    path=MODELS/f'edupredict-{checkpoint}-v1.joblib'
    if not path.exists(): train(checkpoint)
    b=joblib.load(path); df=load_frame(); X=df[b['features']].astype(float); proba=b['pipeline'].predict_proba(X)[:,1]
    band=lambda p: 'high' if p>=0.65 else ('medium' if p>=0.40 else 'low')
    clf=b['pipeline'].named_steps['clf']
    vals = clf.feature_importances_ if hasattr(clf,'feature_importances_') else (np.abs(clf.coef_[0]) if hasattr(clf,'coef_') else np.ones(len(b['features'])))
    vals=vals/(vals.sum() or 1)
    rows=[]
    for i,r in df.iterrows():
        top=np.argsort(vals)[::-1][:3]
        expl=[{'feature_name':b['features'][j],'feature_value':float(X.iloc[i,j]),'shap_value':float(vals[j]*(1 if proba[i]>0.5 else -1)),'impact':'increases_risk' if proba[i]>0.5 else 'decreases_risk','description':f'Model association: {b["features"][j]} influenced this estimate.'} for j in top]
        rows.append({'student_pseudonym':r['student_pseudonym'],'course_code':r['course_code'],'period_code':r['period_code'],'checkpoint':checkpoint,'risk_probability':round(float(proba[i]),4),'risk_band':band(proba[i]),'predicted_outcome':'fail' if proba[i]>=0.45 else 'pass','confidence_score':round(float(max(proba[i],1-proba[i])),4),'model_version':b['version'],'model_name':b['model_name'],'explanations':expl})
    out={'status':'ok','checkpoint':checkpoint,'model_version':b['version'],'model_name':b['model_name'],'count':len(rows),'summary':{'high':sum(r['risk_band']=='high' for r in rows),'medium':sum(r['risk_band']=='medium' for r in rows),'low':sum(r['risk_band']=='low' for r in rows)},'rows':rows,'disclaimer':'Synthetic demo predictions; decision support only, not verdicts.'}
    (REPORTS/f'{b["version"]}-predictions.json').write_text(json.dumps({k:v for k,v in out.items() if k!='rows'}, indent=2)); return out

def status():
    return {'status':'ok','dataset_exists':DATA.exists(),'dataset_dir':str(DATA),'dataset_files':[p.name for p in DATA.glob('*.csv')],'models':[p.name for p in MODELS.glob('*.joblib')],'reports':[p.name for p in REPORTS.glob('*.json')]}

if __name__=='__main__':
    cmd=sys.argv[1] if len(sys.argv)>1 else 'status'; cp=sys.argv[2] if len(sys.argv)>2 else 'week_4'
    fn={'status':lambda:status(),'train':lambda:train(cp),'predict':lambda:predict(cp)}.get(cmd, lambda:{'status':'error','error':f'unknown {cmd}'})
    print(json.dumps(fn(), indent=2))
