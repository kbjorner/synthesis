import time, os
import matplotlib.pyplot as plt

# 2163 total constraints
# iterate = [10, 25, 50, 100, 200, 500, 750, 1000, 1500, 2000, 2163]
iterate = [5]

num_files = len(iterate)
runningTime = [iterate[i] for i in range(num_files)]

def createFile(file):
    g = open(file, "rt")
    constraint = g.readlines()

    for i in range(num_files):
        f = open('mnist{}.smt2'.format(i), 'w') 
        f.write('(set-logic LRA)    (synth-fun rig_mimic ((b0_0 Real) (b0_1 Real) (b0_2 Real) (b0_3 Real) (b0_4 Real) (b0_5 Real) (b0_6 Real) (b0_7 Real) (b0_8 Real) (b0_9 Real) (b0_10 Real) (b0_11 Real) (b0_12 Real) (b0_13 Real) (b0_14 Real) (b0_15 Real) (b0_16 Real) (b0_17 Real) (b0_18 Real) (b0_19 Real) (b0_20 Real) (b0_21 Real) (b0_22 Real) (b0_23 Real) (b0_24 Real) (b0_25 Real) (b0_26 Real) (b0_27 Real) (b1_0 Real) (b1_1 Real) (b1_2 Real) (b1_3 Real) (b1_4 Real) (b1_5 Real) (b1_6 Real) (b1_7 Real) (b1_8 Real) (b1_9 Real) (b1_10 Real) (b1_11 Real) (b1_12 Real) (b1_13 Real) (b1_14 Real) (b1_15 Real) (b1_16 Real) (b1_17 Real) (b1_18 Real) (b1_19 Real) (b1_20 Real) (b1_21 Real) (b1_22 Real) (b1_23 Real) (b1_24 Real) (b1_25 Real) (b1_26 Real) (b1_27 Real) (b2_0 Real) (b2_1 Real) (b2_2 Real) (b2_3 Real) (b2_4 Real) (b2_5 Real) (b2_6 Real) (b2_7 Real) (b2_8 Real) (b2_9 Real) (b2_10 Real) (b2_11 Real) (b2_12 Real) (b2_13 Real) (b2_14 Real) (b2_15 Real) (b2_16 Real) (b2_17 Real) (b2_18 Real) (b2_19 Real) (b2_20 Real) (b2_21 Real) (b2_22 Real) (b2_23 Real) (b2_24 Real) (b2_25 Real) (b2_26 Real) (b2_27 Real) (b3_0 Real) (b3_1 Real) (b3_2 Real) (b3_3 Real) (b3_4 Real) (b3_5 Real) (b3_6 Real) (b3_7 Real) (b3_8 Real) (b3_9 Real) (b3_10 Real) (b3_11 Real) (b3_12 Real) (b3_13 Real) (b3_14 Real) (b3_15 Real) (b3_16 Real) (b3_17 Real) (b3_18 Real) (b3_19 Real) (b3_20 Real) (b3_21 Real) (b3_22 Real) (b3_23 Real) (b3_24 Real) (b3_25 Real) (b3_26 Real) (b3_27 Real) (b4_0 Real) (b4_1 Real) (b4_2 Real) (b4_3 Real) (b4_4 Real) (b4_5 Real) (b4_6 Real) (b4_7 Real) (b4_8 Real) (b4_9 Real) (b4_10 Real) (b4_11 Real) (b4_12 Real) (b4_13 Real) (b4_14 Real) (b4_15 Real) (b4_16 Real) (b4_17 Real) (b4_18 Real) (b4_19 Real) (b4_20 Real) (b4_21 Real) (b4_22 Real) (b4_23 Real) (b4_24 Real) (b4_25 Real) (b4_26 Real) (b4_27 Real) (b5_0 Real) (b5_1 Real) (b5_2 Real) (b5_3 Real) (b5_4 Real) (b5_5 Real) (b5_6 Real) (b5_7 Real) (b5_8 Real) (b5_9 Real) (b5_10 Real) (b5_11 Real) (b5_12 Real) (b5_13 Real) (b5_14 Real) (b5_15 Real) (b5_16 Real) (b5_17 Real) (b5_18 Real) (b5_19 Real) (b5_20 Real) (b5_21 Real) (b5_22 Real) (b5_23 Real) (b5_24 Real) (b5_25 Real) (b5_26 Real) (b5_27 Real) (b6_0 Real) (b6_1 Real) (b6_2 Real) (b6_3 Real) (b6_4 Real) (b6_5 Real) (b6_6 Real) (b6_7 Real) (b6_8 Real) (b6_9 Real) (b6_10 Real) (b6_11 Real) (b6_12 Real) (b6_13 Real) (b6_14 Real) (b6_15 Real) (b6_16 Real) (b6_17 Real) (b6_18 Real) (b6_19 Real) (b6_20 Real) (b6_21 Real) (b6_22 Real) (b6_23 Real) (b6_24 Real) (b6_25 Real) (b6_26 Real) (b6_27 Real) (b7_0 Real) (b7_1 Real) (b7_2 Real) (b7_3 Real) (b7_4 Real) (b7_5 Real) (b7_6 Real) (b7_7 Real) (b7_8 Real) (b7_9 Real) (b7_10 Real) (b7_11 Real) (b7_12 Real) (b7_13 Real) (b7_14 Real) (b7_15 Real) (b7_16 Real) (b7_17 Real) (b7_18 Real) (b7_19 Real) (b7_20 Real) (b7_21 Real) (b7_22 Real) (b7_23 Real) (b7_24 Real) (b7_25 Real) (b7_26 Real) (b7_27 Real) (b8_0 Real) (b8_1 Real) (b8_2 Real) (b8_3 Real) (b8_4 Real) (b8_5 Real) (b8_6 Real) (b8_7 Real) (b8_8 Real) (b8_9 Real) (b8_10 Real) (b8_11 Real) (b8_12 Real) (b8_13 Real) (b8_14 Real) (b8_15 Real) (b8_16 Real) (b8_17 Real) (b8_18 Real) (b8_19 Real) (b8_20 Real) (b8_21 Real) (b8_22 Real) (b8_23 Real) (b8_24 Real) (b8_25 Real) (b8_26 Real) (b8_27 Real) (b9_0 Real) (b9_1 Real) (b9_2 Real) (b9_3 Real) (b9_4 Real) (b9_5 Real) (b9_6 Real) (b9_7 Real) (b9_8 Real) (b9_9 Real) (b9_10 Real) (b9_11 Real) (b9_12 Real) (b9_13 Real) (b9_14 Real) (b9_15 Real) (b9_16 Real) (b9_17 Real) (b9_18 Real) (b9_19 Real) (b9_20 Real) (b9_21 Real) (b9_22 Real) (b9_23 Real) (b9_24 Real) (b9_25 Real) (b9_26 Real) (b9_27 Real) (b10_0 Real) (b10_1 Real) (b10_2 Real) (b10_3 Real) (b10_4 Real) (b10_5 Real) (b10_6 Real) (b10_7 Real) (b10_8 Real) (b10_9 Real) (b10_10 Real) (b10_11 Real) (b10_12 Real) (b10_13 Real) (b10_14 Real) (b10_15 Real) (b10_16 Real) (b10_17 Real) (b10_18 Real) (b10_19 Real) (b10_20 Real) (b10_21 Real) (b10_22 Real) (b10_23 Real) (b10_24 Real) (b10_25 Real) (b10_26 Real) (b10_27 Real) (b11_0 Real) (b11_1 Real) (b11_2 Real) (b11_3 Real) (b11_4 Real) (b11_5 Real) (b11_6 Real) (b11_7 Real) (b11_8 Real) (b11_9 Real) (b11_10 Real) (b11_11 Real) (b11_12 Real) (b11_13 Real) (b11_14 Real) (b11_15 Real) (b11_16 Real) (b11_17 Real) (b11_18 Real) (b11_19 Real) (b11_20 Real) (b11_21 Real) (b11_22 Real) (b11_23 Real) (b11_24 Real) (b11_25 Real) (b11_26 Real) (b11_27 Real) (b12_0 Real) (b12_1 Real) (b12_2 Real) (b12_3 Real) (b12_4 Real) (b12_5 Real) (b12_6 Real) (b12_7 Real) (b12_8 Real) (b12_9 Real) (b12_10 Real) (b12_11 Real) (b12_12 Real) (b12_13 Real) (b12_14 Real) (b12_15 Real) (b12_16 Real) (b12_17 Real) (b12_18 Real) (b12_19 Real) (b12_20 Real) (b12_21 Real) (b12_22 Real) (b12_23 Real) (b12_24 Real) (b12_25 Real) (b12_26 Real) (b12_27 Real) (b13_0 Real) (b13_1 Real) (b13_2 Real) (b13_3 Real) (b13_4 Real) (b13_5 Real) (b13_6 Real) (b13_7 Real) (b13_8 Real) (b13_9 Real) (b13_10 Real) (b13_11 Real) (b13_12 Real) (b13_13 Real) (b13_14 Real) (b13_15 Real) (b13_16 Real) (b13_17 Real) (b13_18 Real) (b13_19 Real) (b13_20 Real) (b13_21 Real) (b13_22 Real) (b13_23 Real) (b13_24 Real) (b13_25 Real) (b13_26 Real) (b13_27 Real) (b14_0 Real) (b14_1 Real) (b14_2 Real) (b14_3 Real) (b14_4 Real) (b14_5 Real) (b14_6 Real) (b14_7 Real) (b14_8 Real) (b14_9 Real) (b14_10 Real) (b14_11 Real) (b14_12 Real) (b14_13 Real) (b14_14 Real) (b14_15 Real) (b14_16 Real) (b14_17 Real) (b14_18 Real) (b14_19 Real) (b14_20 Real) (b14_21 Real) (b14_22 Real) (b14_23 Real) (b14_24 Real) (b14_25 Real) (b14_26 Real) (b14_27 Real) (b15_0 Real) (b15_1 Real) (b15_2 Real) (b15_3 Real) (b15_4 Real) (b15_5 Real) (b15_6 Real) (b15_7 Real) (b15_8 Real) (b15_9 Real) (b15_10 Real) (b15_11 Real) (b15_12 Real) (b15_13 Real) (b15_14 Real) (b15_15 Real) (b15_16 Real) (b15_17 Real) (b15_18 Real) (b15_19 Real) (b15_20 Real) (b15_21 Real) (b15_22 Real) (b15_23 Real) (b15_24 Real) (b15_25 Real) (b15_26 Real) (b15_27 Real) (b16_0 Real) (b16_1 Real) (b16_2 Real) (b16_3 Real) (b16_4 Real) (b16_5 Real) (b16_6 Real) (b16_7 Real) (b16_8 Real) (b16_9 Real) (b16_10 Real) (b16_11 Real) (b16_12 Real) (b16_13 Real) (b16_14 Real) (b16_15 Real) (b16_16 Real) (b16_17 Real) (b16_18 Real) (b16_19 Real) (b16_20 Real) (b16_21 Real) (b16_22 Real) (b16_23 Real) (b16_24 Real) (b16_25 Real) (b16_26 Real) (b16_27 Real) (b17_0 Real) (b17_1 Real) (b17_2 Real) (b17_3 Real) (b17_4 Real) (b17_5 Real) (b17_6 Real) (b17_7 Real) (b17_8 Real) (b17_9 Real) (b17_10 Real) (b17_11 Real) (b17_12 Real) (b17_13 Real) (b17_14 Real) (b17_15 Real) (b17_16 Real) (b17_17 Real) (b17_18 Real) (b17_19 Real) (b17_20 Real) (b17_21 Real) (b17_22 Real) (b17_23 Real) (b17_24 Real) (b17_25 Real) (b17_26 Real) (b17_27 Real) (b18_0 Real) (b18_1 Real) (b18_2 Real) (b18_3 Real) (b18_4 Real) (b18_5 Real) (b18_6 Real) (b18_7 Real) (b18_8 Real) (b18_9 Real) (b18_10 Real) (b18_11 Real) (b18_12 Real) (b18_13 Real) (b18_14 Real) (b18_15 Real) (b18_16 Real) (b18_17 Real) (b18_18 Real) (b18_19 Real) (b18_20 Real) (b18_21 Real) (b18_22 Real) (b18_23 Real) (b18_24 Real) (b18_25 Real) (b18_26 Real) (b18_27 Real) (b19_0 Real) (b19_1 Real) (b19_2 Real) (b19_3 Real) (b19_4 Real) (b19_5 Real) (b19_6 Real) (b19_7 Real) (b19_8 Real) (b19_9 Real) (b19_10 Real) (b19_11 Real) (b19_12 Real) (b19_13 Real) (b19_14 Real) (b19_15 Real) (b19_16 Real) (b19_17 Real) (b19_18 Real) (b19_19 Real) (b19_20 Real) (b19_21 Real) (b19_22 Real) (b19_23 Real) (b19_24 Real) (b19_25 Real) (b19_26 Real) (b19_27 Real) (b20_0 Real) (b20_1 Real) (b20_2 Real) (b20_3 Real) (b20_4 Real) (b20_5 Real) (b20_6 Real) (b20_7 Real) (b20_8 Real) (b20_9 Real) (b20_10 Real) (b20_11 Real) (b20_12 Real) (b20_13 Real) (b20_14 Real) (b20_15 Real) (b20_16 Real) (b20_17 Real) (b20_18 Real) (b20_19 Real) (b20_20 Real) (b20_21 Real) (b20_22 Real) (b20_23 Real) (b20_24 Real) (b20_25 Real) (b20_26 Real) (b20_27 Real) (b21_0 Real) (b21_1 Real) (b21_2 Real) (b21_3 Real) (b21_4 Real) (b21_5 Real) (b21_6 Real) (b21_7 Real) (b21_8 Real) (b21_9 Real) (b21_10 Real) (b21_11 Real) (b21_12 Real) (b21_13 Real) (b21_14 Real) (b21_15 Real) (b21_16 Real) (b21_17 Real) (b21_18 Real) (b21_19 Real) (b21_20 Real) (b21_21 Real) (b21_22 Real) (b21_23 Real) (b21_24 Real) (b21_25 Real) (b21_26 Real) (b21_27 Real) (b22_0 Real) (b22_1 Real) (b22_2 Real) (b22_3 Real) (b22_4 Real) (b22_5 Real) (b22_6 Real) (b22_7 Real) (b22_8 Real) (b22_9 Real) (b22_10 Real) (b22_11 Real) (b22_12 Real) (b22_13 Real) (b22_14 Real) (b22_15 Real) (b22_16 Real) (b22_17 Real) (b22_18 Real) (b22_19 Real) (b22_20 Real) (b22_21 Real) (b22_22 Real) (b22_23 Real) (b22_24 Real) (b22_25 Real) (b22_26 Real) (b22_27 Real) (b23_0 Real) (b23_1 Real) (b23_2 Real) (b23_3 Real) (b23_4 Real) (b23_5 Real) (b23_6 Real) (b23_7 Real) (b23_8 Real) (b23_9 Real) (b23_10 Real) (b23_11 Real) (b23_12 Real) (b23_13 Real) (b23_14 Real) (b23_15 Real) (b23_16 Real) (b23_17 Real) (b23_18 Real) (b23_19 Real) (b23_20 Real) (b23_21 Real) (b23_22 Real) (b23_23 Real) (b23_24 Real) (b23_25 Real) (b23_26 Real) (b23_27 Real) (b24_0 Real) (b24_1 Real) (b24_2 Real) (b24_3 Real) (b24_4 Real) (b24_5 Real) (b24_6 Real) (b24_7 Real) (b24_8 Real) (b24_9 Real) (b24_10 Real) (b24_11 Real) (b24_12 Real) (b24_13 Real) (b24_14 Real) (b24_15 Real) (b24_16 Real) (b24_17 Real) (b24_18 Real) (b24_19 Real) (b24_20 Real) (b24_21 Real) (b24_22 Real) (b24_23 Real) (b24_24 Real) (b24_25 Real) (b24_26 Real) (b24_27 Real) (b25_0 Real) (b25_1 Real) (b25_2 Real) (b25_3 Real) (b25_4 Real) (b25_5 Real) (b25_6 Real) (b25_7 Real) (b25_8 Real) (b25_9 Real) (b25_10 Real) (b25_11 Real) (b25_12 Real) (b25_13 Real) (b25_14 Real) (b25_15 Real) (b25_16 Real) (b25_17 Real) (b25_18 Real) (b25_19 Real) (b25_20 Real) (b25_21 Real) (b25_22 Real) (b25_23 Real) (b25_24 Real) (b25_25 Real) (b25_26 Real) (b25_27 Real) (b26_0 Real) (b26_1 Real) (b26_2 Real) (b26_3 Real) (b26_4 Real) (b26_5 Real) (b26_6 Real) (b26_7 Real) (b26_8 Real) (b26_9 Real) (b26_10 Real) (b26_11 Real) (b26_12 Real) (b26_13 Real) (b26_14 Real) (b26_15 Real) (b26_16 Real) (b26_17 Real) (b26_18 Real) (b26_19 Real) (b26_20 Real) (b26_21 Real) (b26_22 Real) (b26_23 Real) (b26_24 Real) (b26_25 Real) (b26_26 Real) (b26_27 Real) (b27_0 Real) (b27_1 Real) (b27_2 Real) (b27_3 Real) (b27_4 Real) (b27_5 Real) (b27_6 Real) (b27_7 Real) (b27_8 Real) (b27_9 Real) (b27_10 Real) (b27_11 Real) (b27_12 Real) (b27_13 Real) (b27_14 Real) (b27_15 Real) (b27_16 Real) (b27_17 Real) (b27_18 Real) (b27_19 Real) (b27_20 Real) (b27_21 Real) (b27_22 Real) (b27_23 Real) (b27_24 Real) (b27_25 Real) (b27_26 Real) (b27_27 Real)) Bool   ((B Bool) (R Real))    ((B Bool ((<= R R) (and B B) (or B B) (ite B B B)))(R Real ((Variable Real) (ite B R R)))))')

        for j in range(iterate[i]):
            f.write(constraint[j])

        f.write("(check-synth)")
        f.close()

        start_time = time.time()
        os.system('cvc4 --lang=sygus2 mnist{}.smt2'.format(i))

        # instead of printing, put on graph
        runTime = time.time() - start_time
        runningTime[i] = runTime # y

        print("--- %s seconds ---" % (runningTime)) # y

    g.close()

def plotRunTime():
    plt.scatter(iterate, runningTime)
    plt.xlabel('Number of Constraints')
    plt.ylabel('Running Time (seconds)')
    plt.title('CVC4 Runtime with Different Number of Constraints (MNIST)')
    plt.savefig('MNIST')
    plt.show()

createFile("allConstraints.txt")

# print("x: {}; y: {}".format(iterate[0], runningTime[0]))

plotRunTime()