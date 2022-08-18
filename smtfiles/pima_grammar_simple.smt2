(set-logic LRA) (synth-fun rig_mimic ((Pregnancies Real) (Glucose Real) (BloodPressure Real) (SkinThickness Real) (Insulin Real) (BodyMassIndex Real) (DiabetesPedigreeFunction Real) (Age Real)) 
Bool ((B Bool) (BC Bool) (P Real) (G Real) (BP Real) (ST Real) (I Real) (BMI Real) (DPF Real) (A Real) (PC Bool) (GC Bool) (BPC Bool) (STC Bool) (IC Bool) (BMIC Bool) (DPFC Bool) (AC Bool))((B Bool ((Constant Bool) PC GC BPC STC IC BMIC DPFC AC (ite BC B B) ))(BC Bool (PC GC BPC STC IC BMIC DPFC AC))
(P Real (1.0 3.0 6.0)) 
(G Real (99.75 117.0 140.25))
(BP Real (64.0 72.20259208731241 80.0)) 
(ST Real (25.0 29.153419593345657 32.0))
(I Real (121.5 155.5482233502538 155.5482233502538)) 
(BMI Real (27.5 32.4 36.6)) 
(DPF Real (0.24375 0.3725 0.62625))
(A Real (24.0 29.0 41.0))
(PC Bool ((<= P Pregnancies)(>= P Pregnancies))) 
(GC Bool ((<= G Glucose)(>= G Glucose))) 
(BPC Bool ((<= BP BloodPressure)(>= BP BloodPressure)))
(STC Bool ((<= ST SkinThickness)(>= ST SkinThickness))) 
(IC Bool ((<= I Insulin)(>= I Insulin))) 
(BMIC Bool ((<= BMI BodyMassIndex)(>= BMI BodyMassIndex)))
(DPFC Bool ((<= DPF DiabetesPedigreeFunction)(>= DPF DiabetesPedigreeFunction)))
(AC Bool ((<= A Age)(>= A Age)))))