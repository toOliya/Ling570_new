class ViterbiTest(unittest.TestCase):
    def test_simpleTransition(self):
        # arrange
        # He
        # hmm => tran => bos pn 1.0 emmiss => pn he 1.0
        # [ state { previousPos, currentPos, symbol, stateProbability } ]
        hmm = """state_num=6
sym_num=11
init_line_num=2
trans_line_num=13
emiss_line_num=11

\init
BOS     0.9 

\\transition
BOS N 1.0
N V 0.4
N D 0.5

\emission
DT  the 0.7
DT  a   0.1
N   a   1.0""".split("\n")

        vitTest = viterbi.Viterbi()
        for i in range(0, len(hmm)):
            line = hmm[i]
            vitTest.readInput(line)

        # act
        result = vitTest.processLine("a")

        # assert
        # [ state { previousPos: BOS, currentPos: N, symbol: a, stateProbability: 1.0 } ]

        self.assertTrue(len(result) == 1)
        self.assertTrue(result[0][0] == "BOS")
        self.assertTrue(result[0][1] == "N")
        self.assertTrue(result[0][2] == 1.0)
        self.assertTrue(result[0][3] == "a")

    def test_slightlyMoreComplexTransition(self):
        # arrange
        # He
        # hmm => tran => bos pn 1.0 emmiss => pn he 1.0
        # [ state { previousPos, currentPos, symbol, stateProbability } ]
        hmm = """state_num=6
sym_num=11
init_line_num=2
trans_line_num=13
emiss_line_num=11

\init
BOS     0.9 

\\transition
BOS N 1.0
N V 0.4
N D 0.5
V PN 1.0

\emission
DT  the 0.3
DT  a   0.7
N   a   .4
N   test .6
V   walk 1.0""".split("\n")

        # a\N walk\V
        # P(walk | V) == 1.0 && P(V | N) == .4

        vitTest = viterbi.Viterbi()
        for i in range(0, len(hmm)):
            line = hmm[i]
            vitTest.readInput(line)

        # act
        result = vitTest.processLine("a walk")

        # assert
        # [ state { previousPos: BOS, currentPos: N, symbol: a, stateProbability: 1.0 } ]

        self.assertTrue(len(result) == 1)
        self.assertTrue(result[0][0] == "BOS")
        self.assertTrue(result[0][1] == "N")
        self.assertTrue(result[0][2] == 1.0)
        self.assertTrue(result[0][3] == "a")

	def test_getPrevPathState(self):
		# arrange
		VitInput = 'a'

       		hmm = """state_num=6
sym_num=11
init_line_num=2
trans_line_num=13
emiss_line_num=11

\init
BOS     0.9 

\\transition
BOS N 1.0
N V 0.4
N D 0.5

\emission
DT  the 0.7
DT  a   0.1
N   a   1.0""".split("\n")


		VitTest = viterbi.Viterbi()
		for i in range(0, len(hmm)):
			line = hmm[i]
			VitTest.readInput(line)

		# act
		actualResult = VitTest.getPrevPathState(VitInput)
#		print actualResult

		# assert
		self.assertTrue(actualResult == ['DT', 'N'])


        def test_getPrevPathWithHighestProb(self):
                # arrange
                VitInput = ['DT', 'N']

                hmm = """state_num=6
sym_num=11
init_line_num=2
trans_line_num=13
emiss_line_num=11

\init
BOS     0.9 

\\transition
BOS N 1.0
N V 0.4
N D 0.5

\emission
DT  the 0.7
DT  a   0.1
N   a   1.0""".split("\n")

                VitTest = viterbi.Viterbi()
                for i in range(0, len(hmm)):
                        line = hmm[i]
                        VitTest.readInput(line)

                # act
		
                actualResult = VitTest.getPrevPathWithHighestProb(VitInput, 'BOS')
#		print VitTest.current_trans_dict
                print actualResult

                # assert
                self.assertTrue(actualResult == ('N', 1.0))



class Utilities(unittest.TestCase):
    def test_movesToEmissVals1(self):
        # arrange
        hmmInput = """state_num=6
sym_num=11
init_line_num=2
trans_line_num=13
emiss_line_num=11

\init
BOS     0.9 

\\transition
BOS N 1.0
N V 0.4
N D 0.5

\emission
DT  the 0.7
DT  a   0.1
N   a   1.0""".split("\n")

        hmmFactory = utilities.Utilities()

        # act
        hmmFactory.readInput(hmmInput[0])
        hmmFactory.readInput(hmmInput[1])
        hmmFactory.readInput(hmmInput[2])
        hmmFactory.readInput(hmmInput[3])
        hmmFactory.readInput(hmmInput[4])
        hmmFactory.readInput(hmmInput[5])
        hmmFactory.readInput(hmmInput[6])
        hmmFactory.readInput(hmmInput[7])
        hmmFactory.readInput(hmmInput[8])
        hmmFactory.readInput(hmmInput[9])
        hmmFactory.readInput(hmmInput[10])
        hmmFactory.readInput(hmmInput[11])
        hmmFactory.readInput(hmmInput[12])
        hmmFactory.readInput(hmmInput[13])
        hmmFactory.readInput(hmmInput[14])
        hmmFactory.readInput(hmmInput[15])
        hmmFactory.readInput(hmmInput[16])

        # assert
                                                                                                                    
        self.assertTrue(hmmFactory.current_symb_dict["the"]["DT"] == 0.7)
        self.assertTrue(hmmFactory.current_symb_dict["a"]["DT"] == 0.1)