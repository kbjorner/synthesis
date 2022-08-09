{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 27,
   "id": "2bad1d51",
   "metadata": {},
   "outputs": [],
   "source": [
    "import time, os\n",
    "import numpy as np\n",
    "import random\n",
    "import matplotlib.pyplot as plt"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 39,
   "id": "4746b2f2",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[1923, 655, 16, 390, 2149, 1775, 1180, 1956, 1018, 56]\n",
      "[175, 1648, 2093, 154, 112, 2135, 1841, 874, 377, 1114, 1735, 2045, 604, 1887, 1171, 1354, 814, 533, 263, 1532, 648, 1311, 233, 1205, 247]\n",
      "[1686, 1875, 1921, 1087, 245, 1585, 666, 1745, 665, 1531, 490, 2123, 1920, 880, 1590, 1470, 788, 1486, 2046, 1477, 1440, 312, 1340, 1478, 1325, 1294, 237, 813, 405, 1633, 978, 1297, 1225, 959, 1924, 1632, 1907, 1591, 1665, 1705, 904, 1698, 330, 492, 461, 1539, 1478, 1498, 731, 871]\n",
      "[932, 1601, 2150, 1767, 1876, 1130, 413, 79, 695, 1570, 1985, 347, 518, 791, 406, 1077, 383, 986, 996, 1084, 387, 2006, 1162, 1018, 1951, 1109, 1229, 576, 748, 1249, 64, 440, 2061, 802, 564, 1644, 1267, 1568, 787, 1300, 131, 392, 1749, 625, 2072, 659, 1094, 1104, 2024, 1198, 139, 378, 1276, 1863, 1853, 859, 1041, 129, 1975, 953, 960, 1686, 1170, 1419, 679, 804, 1784, 150, 1546, 2083, 98, 716, 116, 2154, 1353, 2098, 841, 2086, 1266, 24, 675, 2155, 1004, 2028, 835, 1149, 1744, 2080, 1663, 244, 1648, 88, 53, 1294, 514, 568, 1647, 1865, 289, 230]\n"
     ]
    }
   ],
   "source": [
    "iterate = [10, 25, 50, 100]\n",
    "n = 10\n",
    "df = \n",
    "# rn 10 times each iterate number to get 5 num summary and plot mean with variance\n",
    "for i in iterate:\n",
    "    arr = []*i\n",
    "    for j in range(i):\n",
    "        arr.append(random.randrange(0, 2163))\n",
    "    print(arr)\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 36,
   "id": "e17ce252",
   "metadata": {},
   "outputs": [],
   "source": [
    "# 2163 total constraints\n",
    "# iterate = [10, 25, 50, 100, 200, 500, 750, 1000, 1500, 2000, 2163]\n",
    "iterate = [10] #, 25, 50, 100]\n",
    "# rn 10 times each iterate number to get 5 num summary and plot mean with variance\n",
    "for i in iterate:\n",
    "    arr = []*i\n",
    "    for j in range(i):\n",
    "        arr.append(random.randrange(0, 2163))\n",
    "\n",
    "# num_files = len(iterate)\n",
    "runningTime = iterate\n",
    "\n",
    "def createFile(file):\n",
    "    g = open(file, \"rt\")\n",
    "    constraint = g.readlines()\n",
    "\n",
    "    for i in range(num_files):\n",
    "        f = open('mnist{}.smt2'.format(i), 'w')\n",
    "        # have this in a file to read from\n",
    "        g = open(\"smtGuts.txt\", \"r\")\n",
    "        for line in g:\n",
    "            f.write(line)\n",
    "\n",
    "        for j in range(iterate[i]):\n",
    "            f.write(constraint[j])\n",
    "\n",
    "        f.write(\"(check-synth)\")\n",
    "        f.close()\n",
    "\n",
    "        start_time = time.time()\n",
    "        os.system('../../cvc5/build/bin/cvc5 --lang=sygus2 mnist{}.smt2'.format(i))\n",
    "\n",
    "        # instead of printing, put on graph\n",
    "        runTime = time.time() - start_time\n",
    "        runningTime[i] = runTime # y\n",
    "\n",
    "#         print(\"--- %s seconds ---\" % (runningTime)) # y\n",
    "\n",
    "\n",
    "    g.close()\n",
    "\n",
    "def plotRunTime():\n",
    "#     z = np.polyfit(iterate, runningTime, 1)\n",
    "#     p = np.poly1d(z)\n",
    "    \n",
    "    plt.rcParams.update({'axes.labelsize' : 14, 'axes.titlesize': 14, 'font.family': 'serif'})\n",
    "    c = '#ff0000'\n",
    "    plt.scatter(iterate, runningTime, color = c)\n",
    "#     plt.plot(iterate, p(iterate), linestyle = '--', color = c)\n",
    "    plt.xlabel('Number of Constraints')\n",
    "    plt.ylabel('Running Time (seconds)')\n",
    "    plt.title('CVC4 Runtime with Different Number of Constraints (MNIST)')\n",
    "#     plt.xticks(iterate, ['10', '25', '50', '100'])\n",
    "    \n",
    "    plt.margins(0)\n",
    "    plt.savefig('MNIST')\n",
    "    plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "id": "7d4301db",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "(\n",
      "(define-fun rig_mimic ((b0_0 Real) (b0_1 Real) (b0_2 Real) (b0_3 Real) (b0_4 Real) (b0_5 Real) (b0_6 Real) (b0_7 Real) (b0_8 Real) (b0_9 Real) (b0_10 Real) (b0_11 Real) (b0_12 Real) (b0_13 Real) (b0_14 Real) (b0_15 Real) (b0_16 Real) (b0_17 Real) (b0_18 Real) (b0_19 Real) (b0_20 Real) (b0_21 Real) (b0_22 Real) (b0_23 Real) (b0_24 Real) (b0_25 Real) (b0_26 Real) (b0_27 Real) (b1_0 Real) (b1_1 Real) (b1_2 Real) (b1_3 Real) (b1_4 Real) (b1_5 Real) (b1_6 Real) (b1_7 Real) (b1_8 Real) (b1_9 Real) (b1_10 Real) (b1_11 Real) (b1_12 Real) (b1_13 Real) (b1_14 Real) (b1_15 Real) (b1_16 Real) (b1_17 Real) (b1_18 Real) (b1_19 Real) (b1_20 Real) (b1_21 Real) (b1_22 Real) (b1_23 Real) (b1_24 Real) (b1_25 Real) (b1_26 Real) (b1_27 Real) (b2_0 Real) (b2_1 Real) (b2_2 Real) (b2_3 Real) (b2_4 Real) (b2_5 Real) (b2_6 Real) (b2_7 Real) (b2_8 Real) (b2_9 Real) (b2_10 Real) (b2_11 Real) (b2_12 Real) (b2_13 Real) (b2_14 Real) (b2_15 Real) (b2_16 Real) (b2_17 Real) (b2_18 Real) (b2_19 Real) (b2_20 Real) (b2_21 Real) (b2_22 Real) (b2_23 Real) (b2_24 Real) (b2_25 Real) (b2_26 Real) (b2_27 Real) (b3_0 Real) (b3_1 Real) (b3_2 Real) (b3_3 Real) (b3_4 Real) (b3_5 Real) (b3_6 Real) (b3_7 Real) (b3_8 Real) (b3_9 Real) (b3_10 Real) (b3_11 Real) (b3_12 Real) (b3_13 Real) (b3_14 Real) (b3_15 Real) (b3_16 Real) (b3_17 Real) (b3_18 Real) (b3_19 Real) (b3_20 Real) (b3_21 Real) (b3_22 Real) (b3_23 Real) (b3_24 Real) (b3_25 Real) (b3_26 Real) (b3_27 Real) (b4_0 Real) (b4_1 Real) (b4_2 Real) (b4_3 Real) (b4_4 Real) (b4_5 Real) (b4_6 Real) (b4_7 Real) (b4_8 Real) (b4_9 Real) (b4_10 Real) (b4_11 Real) (b4_12 Real) (b4_13 Real) (b4_14 Real) (b4_15 Real) (b4_16 Real) (b4_17 Real) (b4_18 Real) (b4_19 Real) (b4_20 Real) (b4_21 Real) (b4_22 Real) (b4_23 Real) (b4_24 Real) (b4_25 Real) (b4_26 Real) (b4_27 Real) (b5_0 Real) (b5_1 Real) (b5_2 Real) (b5_3 Real) (b5_4 Real) (b5_5 Real) (b5_6 Real) (b5_7 Real) (b5_8 Real) (b5_9 Real) (b5_10 Real) (b5_11 Real) (b5_12 Real) (b5_13 Real) (b5_14 Real) (b5_15 Real) (b5_16 Real) (b5_17 Real) (b5_18 Real) (b5_19 Real) (b5_20 Real) (b5_21 Real) (b5_22 Real) (b5_23 Real) (b5_24 Real) (b5_25 Real) (b5_26 Real) (b5_27 Real) (b6_0 Real) (b6_1 Real) (b6_2 Real) (b6_3 Real) (b6_4 Real) (b6_5 Real) (b6_6 Real) (b6_7 Real) (b6_8 Real) (b6_9 Real) (b6_10 Real) (b6_11 Real) (b6_12 Real) (b6_13 Real) (b6_14 Real) (b6_15 Real) (b6_16 Real) (b6_17 Real) (b6_18 Real) (b6_19 Real) (b6_20 Real) (b6_21 Real) (b6_22 Real) (b6_23 Real) (b6_24 Real) (b6_25 Real) (b6_26 Real) (b6_27 Real) (b7_0 Real) (b7_1 Real) (b7_2 Real) (b7_3 Real) (b7_4 Real) (b7_5 Real) (b7_6 Real) (b7_7 Real) (b7_8 Real) (b7_9 Real) (b7_10 Real) (b7_11 Real) (b7_12 Real) (b7_13 Real) (b7_14 Real) (b7_15 Real) (b7_16 Real) (b7_17 Real) (b7_18 Real) (b7_19 Real) (b7_20 Real) (b7_21 Real) (b7_22 Real) (b7_23 Real) (b7_24 Real) (b7_25 Real) (b7_26 Real) (b7_27 Real) (b8_0 Real) (b8_1 Real) (b8_2 Real) (b8_3 Real) (b8_4 Real) (b8_5 Real) (b8_6 Real) (b8_7 Real) (b8_8 Real) (b8_9 Real) (b8_10 Real) (b8_11 Real) (b8_12 Real) (b8_13 Real) (b8_14 Real) (b8_15 Real) (b8_16 Real) (b8_17 Real) (b8_18 Real) (b8_19 Real) (b8_20 Real) (b8_21 Real) (b8_22 Real) (b8_23 Real) (b8_24 Real) (b8_25 Real) (b8_26 Real) (b8_27 Real) (b9_0 Real) (b9_1 Real) (b9_2 Real) (b9_3 Real) (b9_4 Real) (b9_5 Real) (b9_6 Real) (b9_7 Real) (b9_8 Real) (b9_9 Real) (b9_10 Real) (b9_11 Real) (b9_12 Real) (b9_13 Real) (b9_14 Real) (b9_15 Real) (b9_16 Real) (b9_17 Real) (b9_18 Real) (b9_19 Real) (b9_20 Real) (b9_21 Real) (b9_22 Real) (b9_23 Real) (b9_24 Real) (b9_25 Real) (b9_26 Real) (b9_27 Real) (b10_0 Real) (b10_1 Real) (b10_2 Real) (b10_3 Real) (b10_4 Real) (b10_5 Real) (b10_6 Real) (b10_7 Real) (b10_8 Real) (b10_9 Real) (b10_10 Real) (b10_11 Real) (b10_12 Real) (b10_13 Real) (b10_14 Real) (b10_15 Real) (b10_16 Real) (b10_17 Real) (b10_18 Real) (b10_19 Real) (b10_20 Real) (b10_21 Real) (b10_22 Real) (b10_23 Real) (b10_24 Real) (b10_25 Real) (b10_26 Real) (b10_27 Real) (b11_0 Real) (b11_1 Real) (b11_2 Real) (b11_3 Real) (b11_4 Real) (b11_5 Real) (b11_6 Real) (b11_7 Real) (b11_8 Real) (b11_9 Real) (b11_10 Real) (b11_11 Real) (b11_12 Real) (b11_13 Real) (b11_14 Real) (b11_15 Real) (b11_16 Real) (b11_17 Real) (b11_18 Real) (b11_19 Real) (b11_20 Real) (b11_21 Real) (b11_22 Real) (b11_23 Real) (b11_24 Real) (b11_25 Real) (b11_26 Real) (b11_27 Real) (b12_0 Real) (b12_1 Real) (b12_2 Real) (b12_3 Real) (b12_4 Real) (b12_5 Real) (b12_6 Real) (b12_7 Real) (b12_8 Real) (b12_9 Real) (b12_10 Real) (b12_11 Real) (b12_12 Real) (b12_13 Real) (b12_14 Real) (b12_15 Real) (b12_16 Real) (b12_17 Real) (b12_18 Real) (b12_19 Real) (b12_20 Real) (b12_21 Real) (b12_22 Real) (b12_23 Real) (b12_24 Real) (b12_25 Real) (b12_26 Real) (b12_27 Real) (b13_0 Real) (b13_1 Real) (b13_2 Real) (b13_3 Real) (b13_4 Real) (b13_5 Real) (b13_6 Real) (b13_7 Real) (b13_8 Real) (b13_9 Real) (b13_10 Real) (b13_11 Real) (b13_12 Real) (b13_13 Real) (b13_14 Real) (b13_15 Real) (b13_16 Real) (b13_17 Real) (b13_18 Real) (b13_19 Real) (b13_20 Real) (b13_21 Real) (b13_22 Real) (b13_23 Real) (b13_24 Real) (b13_25 Real) (b13_26 Real) (b13_27 Real) (b14_0 Real) (b14_1 Real) (b14_2 Real) (b14_3 Real) (b14_4 Real) (b14_5 Real) (b14_6 Real) (b14_7 Real) (b14_8 Real) (b14_9 Real) (b14_10 Real) (b14_11 Real) (b14_12 Real) (b14_13 Real) (b14_14 Real) (b14_15 Real) (b14_16 Real) (b14_17 Real) (b14_18 Real) (b14_19 Real) (b14_20 Real) (b14_21 Real) (b14_22 Real) (b14_23 Real) (b14_24 Real) (b14_25 Real) (b14_26 Real) (b14_27 Real) (b15_0 Real) (b15_1 Real) (b15_2 Real) (b15_3 Real) (b15_4 Real) (b15_5 Real) (b15_6 Real) (b15_7 Real) (b15_8 Real) (b15_9 Real) (b15_10 Real) (b15_11 Real) (b15_12 Real) (b15_13 Real) (b15_14 Real) (b15_15 Real) (b15_16 Real) (b15_17 Real) (b15_18 Real) (b15_19 Real) (b15_20 Real) (b15_21 Real) (b15_22 Real) (b15_23 Real) (b15_24 Real) (b15_25 Real) (b15_26 Real) (b15_27 Real) (b16_0 Real) (b16_1 Real) (b16_2 Real) (b16_3 Real) (b16_4 Real) (b16_5 Real) (b16_6 Real) (b16_7 Real) (b16_8 Real) (b16_9 Real) (b16_10 Real) (b16_11 Real) (b16_12 Real) (b16_13 Real) (b16_14 Real) (b16_15 Real) (b16_16 Real) (b16_17 Real) (b16_18 Real) (b16_19 Real) (b16_20 Real) (b16_21 Real) (b16_22 Real) (b16_23 Real) (b16_24 Real) (b16_25 Real) (b16_26 Real) (b16_27 Real) (b17_0 Real) (b17_1 Real) (b17_2 Real) (b17_3 Real) (b17_4 Real) (b17_5 Real) (b17_6 Real) (b17_7 Real) (b17_8 Real) (b17_9 Real) (b17_10 Real) (b17_11 Real) (b17_12 Real) (b17_13 Real) (b17_14 Real) (b17_15 Real) (b17_16 Real) (b17_17 Real) (b17_18 Real) (b17_19 Real) (b17_20 Real) (b17_21 Real) (b17_22 Real) (b17_23 Real) (b17_24 Real) (b17_25 Real) (b17_26 Real) (b17_27 Real) (b18_0 Real) (b18_1 Real) (b18_2 Real) (b18_3 Real) (b18_4 Real) (b18_5 Real) (b18_6 Real) (b18_7 Real) (b18_8 Real) (b18_9 Real) (b18_10 Real) (b18_11 Real) (b18_12 Real) (b18_13 Real) (b18_14 Real) (b18_15 Real) (b18_16 Real) (b18_17 Real) (b18_18 Real) (b18_19 Real) (b18_20 Real) (b18_21 Real) (b18_22 Real) (b18_23 Real) (b18_24 Real) (b18_25 Real) (b18_26 Real) (b18_27 Real) (b19_0 Real) (b19_1 Real) (b19_2 Real) (b19_3 Real) (b19_4 Real) (b19_5 Real) (b19_6 Real) (b19_7 Real) (b19_8 Real) (b19_9 Real) (b19_10 Real) (b19_11 Real) (b19_12 Real) (b19_13 Real) (b19_14 Real) (b19_15 Real) (b19_16 Real) (b19_17 Real) (b19_18 Real) (b19_19 Real) (b19_20 Real) (b19_21 Real) (b19_22 Real) (b19_23 Real) (b19_24 Real) (b19_25 Real) (b19_26 Real) (b19_27 Real) (b20_0 Real) (b20_1 Real) (b20_2 Real) (b20_3 Real) (b20_4 Real) (b20_5 Real) (b20_6 Real) (b20_7 Real) (b20_8 Real) (b20_9 Real) (b20_10 Real) (b20_11 Real) (b20_12 Real) (b20_13 Real) (b20_14 Real) (b20_15 Real) (b20_16 Real) (b20_17 Real) (b20_18 Real) (b20_19 Real) (b20_20 Real) (b20_21 Real) (b20_22 Real) (b20_23 Real) (b20_24 Real) (b20_25 Real) (b20_26 Real) (b20_27 Real) (b21_0 Real) (b21_1 Real) (b21_2 Real) (b21_3 Real) (b21_4 Real) (b21_5 Real) (b21_6 Real) (b21_7 Real) (b21_8 Real) (b21_9 Real) (b21_10 Real) (b21_11 Real) (b21_12 Real) (b21_13 Real) (b21_14 Real) (b21_15 Real) (b21_16 Real) (b21_17 Real) (b21_18 Real) (b21_19 Real) (b21_20 Real) (b21_21 Real) (b21_22 Real) (b21_23 Real) (b21_24 Real) (b21_25 Real) (b21_26 Real) (b21_27 Real) (b22_0 Real) (b22_1 Real) (b22_2 Real) (b22_3 Real) (b22_4 Real) (b22_5 Real) (b22_6 Real) (b22_7 Real) (b22_8 Real) (b22_9 Real) (b22_10 Real) (b22_11 Real) (b22_12 Real) (b22_13 Real) (b22_14 Real) (b22_15 Real) (b22_16 Real) (b22_17 Real) (b22_18 Real) (b22_19 Real) (b22_20 Real) (b22_21 Real) (b22_22 Real) (b22_23 Real) (b22_24 Real) (b22_25 Real) (b22_26 Real) (b22_27 Real) (b23_0 Real) (b23_1 Real) (b23_2 Real) (b23_3 Real) (b23_4 Real) (b23_5 Real) (b23_6 Real) (b23_7 Real) (b23_8 Real) (b23_9 Real) (b23_10 Real) (b23_11 Real) (b23_12 Real) (b23_13 Real) (b23_14 Real) (b23_15 Real) (b23_16 Real) (b23_17 Real) (b23_18 Real) (b23_19 Real) (b23_20 Real) (b23_21 Real) (b23_22 Real) (b23_23 Real) (b23_24 Real) (b23_25 Real) (b23_26 Real) (b23_27 Real) (b24_0 Real) (b24_1 Real) (b24_2 Real) (b24_3 Real) (b24_4 Real) (b24_5 Real) (b24_6 Real) (b24_7 Real) (b24_8 Real) (b24_9 Real) (b24_10 Real) (b24_11 Real) (b24_12 Real) (b24_13 Real) (b24_14 Real) (b24_15 Real) (b24_16 Real) (b24_17 Real) (b24_18 Real) (b24_19 Real) (b24_20 Real) (b24_21 Real) (b24_22 Real) (b24_23 Real) (b24_24 Real) (b24_25 Real) (b24_26 Real) (b24_27 Real) (b25_0 Real) (b25_1 Real) (b25_2 Real) (b25_3 Real) (b25_4 Real) (b25_5 Real) (b25_6 Real) (b25_7 Real) (b25_8 Real) (b25_9 Real) (b25_10 Real) (b25_11 Real) (b25_12 Real) (b25_13 Real) (b25_14 Real) (b25_15 Real) (b25_16 Real) (b25_17 Real) (b25_18 Real) (b25_19 Real) (b25_20 Real) (b25_21 Real) (b25_22 Real) (b25_23 Real) (b25_24 Real) (b25_25 Real) (b25_26 Real) (b25_27 Real) (b26_0 Real) (b26_1 Real) (b26_2 Real) (b26_3 Real) (b26_4 Real) (b26_5 Real) (b26_6 Real) (b26_7 Real) (b26_8 Real) (b26_9 Real) (b26_10 Real) (b26_11 Real) (b26_12 Real) (b26_13 Real) (b26_14 Real) (b26_15 Real) (b26_16 Real) (b26_17 Real) (b26_18 Real) (b26_19 Real) (b26_20 Real) (b26_21 Real) (b26_22 Real) (b26_23 Real) (b26_24 Real) (b26_25 Real) (b26_26 Real) (b26_27 Real) (b27_0 Real) (b27_1 Real) (b27_2 Real) (b27_3 Real) (b27_4 Real) (b27_5 Real) (b27_6 Real) (b27_7 Real) (b27_8 Real) (b27_9 Real) (b27_10 Real) (b27_11 Real) (b27_12 Real) (b27_13 Real) (b27_14 Real) (b27_15 Real) (b27_16 Real) (b27_17 Real) (b27_18 Real) (b27_19 Real) (b27_20 Real) (b27_21 Real) (b27_22 Real) (b27_23 Real) (b27_24 Real) (b27_25 Real) (b27_26 Real) (b27_27 Real)) Bool (let ((_let_1 (<= b6_11 b6_10))) (ite (<= b6_12 b7_12) (ite (<= b5_14 b13_15) (ite (<= b5_14 b6_9) (<= b6_13 b0_0) (<= b5_14 b15_14)) _let_1) _let_1)))\n",
      ")\n"
     ]
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "createFile(\"allConstraints.txt\")\n",
    "\n",
    "# print(\"x: {}; y: {}\".format(iterate[0], runningTime[0]))\n",
    "\n",
    "plotRunTime()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
