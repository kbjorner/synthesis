(set-logic LRA) (synth-fun rig_mimic ((Pregnancies Real) (Glucose Real) (BloodPressure Real) (SkinThickness Real) (Insulin Real) (BodyMassIndex Real) (DiabetesPedigreeFunction Real) (Age Real)) 
Bool ((B Bool) (BC Bool) (P Real) (G Real) (BP Real) (ST Real) (I Real) (BMI Real) (DPF Real) (A Real) (PC Bool) (GC Bool) (BPC Bool) (STC Bool) (IC Bool) (BMIC Bool) (DPFC Bool) (AC Bool))((B Bool ((Constant Bool) PC GC BPC STC IC BMIC DPFC AC (ite BC B B) ))(BC Bool (PC GC BPC STC IC BMIC DPFC AC))
(P Real ()) 
(G Real ())
(BP Real ()) 
(ST Real ())
(I Real ()) 
(BMI Real ()) 
(DPF Real ())
(A Real ())
(PC Bool ((<= P Pregnancies)(>= P Pregnancies))) 
(GC Bool ((<= G Glucose)(>= G Glucose))) 
(BPC Bool ((<= BP BloodPressure)(>= BP BloodPressure)))
(STC Bool ((<= ST SkinThickness)(>= ST SkinThickness))) 
(IC Bool ((<= I Insulin)(>= I Insulin))) 
(BMIC Bool ((<= BMI BodyMassIndex)(>= BMI BodyMassIndex)))
(DPFC Bool ((<= DPF DiabetesPedigreeFunction)(>= DPF DiabetesPedigreeFunction)))
(AC Bool ((<= A Age)(>= A Age)))))