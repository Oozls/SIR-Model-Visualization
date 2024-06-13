# -*- coding: UTF-8 -*-
from manim import *
import math

# manim ./Main.py CLASSNAME -pqm

class Test(Scene):
    def construct(self):
        self.list_data = {}
        S0 = ValueTracker(999999)
        self.Sd = ValueTracker(-0.25/(S0.get_value()+1)*S0.get_value()*1)
        self.beta = ValueTracker(0.25)
        
        #PLOTS
        width1 = 240.0

        axes1 = Axes(
            x_range=[0, width1, width1/5],
            y_range=[0, 1000000, 250000],
            x_length=7,
            tips=False)
        axes1.add_coordinates()
        axes1_labels = axes1.get_axis_labels(x_label="t", y_label="S").shift(LEFT*0.125,DOWN*0.125)

        N1_interval = 1

        graph1_S = always_redraw(lambda: axes1.plot(
            lambda x: self.sir_model(x, width1, round(S0.get_value()), 1, round(self.beta.get_value(), 2), 0.05, N1_interval, "S"),
            x_range=[0, width1, N1_interval],
            use_smoothing=False,
            color=YELLOW))
        graph1_Sl = always_redraw(lambda: axes1.get_graph_label(graph=graph1_S,
                                        label=MathTex(r"S", font_size=50),
                                        x_val=width1,
                                        direction=UP*0.5,
                                        color=YELLOW))

        graph1_I = always_redraw(lambda: axes1.plot(
            lambda x: self.sir_model(x, width1, round(S0.get_value()), 1, round(self.beta.get_value(), 2), 0.05, N1_interval, "I"),
            x_range=[0, width1, N1_interval],
            use_smoothing=False,
            color=GREEN))
        graph1_Il = always_redraw(lambda: axes1.get_graph_label(graph=graph1_I,
                                        label=MathTex(r"I", font_size=50),
                                        x_val=width1*0.95,
                                        direction=UP*0.5,
                                        color=GREEN))

        graph1_R = always_redraw(lambda: axes1.plot(
            lambda x: self.sir_model(x, width1, round(S0.get_value()), 1, round(self.beta.get_value(), 2), 0.05, N1_interval, "R"),
            x_range=[0, width1, N1_interval],
            use_smoothing=False,
            color=BLUE))
        graph1_Rl = always_redraw(lambda: axes1.get_graph_label(graph=graph1_R,
                                        label=MathTex(r"R", font_size=50),
                                        x_val=width1,
                                        color=BLUE))
        
        print(np.around(np.concatenate((axes1.point_to_coords(np.array([width1/2, 100, 0])), [0]))))

        line1 = axes1.plot_line_graph(x_values=[48,48], y_values=[0,1000000], add_vertex_dots=False, line_color=RED)

        graph1_group = VGroup(axes1, graph1_S, graph1_I, graph1_R, graph1_Sl, graph1_Il, graph1_Rl, axes1_labels, line1)
        graph1_group.shift(LEFT*1.5)

        # TEXTS
        text1 = always_redraw(lambda: MathTex(r'&\frac{dS}{dt} = -\frac{\beta}{N} \cdot S \cdot I\\',
                                              r'&              = ' + str(round(self.Sd.get_value(), 5)) + r'\\'
                                              r'&N \approx S_0 = ' + str(round(S0.get_value())) + r'\\',
                                              r'&I_0 = 1\\',
                                              r'&\beta = ' + str(round(self.beta.get_value(), 2)) + r'\\',
                                              r'&R_0 = 0.5\\',
                                              font_size=30).shift(RIGHT*4.25, UP*1.75))

        '''graph2 = always_redraw(lambda: axes1.plot(
            lambda x: self.sir_model(50, S0.get_value(), 1, 1.2, 0)['S'][ min( round(x), len( self.sir_model(50, S0.get_value(), 1, 1.2, 0)['S'] )-1 ) ], 
            x_range=[0, 50, 1],
            use_smoothing=False,
            color=BLUE))
        
        graph2_group = VGroup(graph2)
        graph2_group.shift(LEFT*1.5)'''

        # PLAYING
        self.play(Write(text1), run_time=5)
        self.play(DrawBorderThenFill(axes1), Write(axes1_labels))
        self.play(Create(graph1_S), Create(graph1_I), Create(graph1_R), Create(line1), Write(graph1_Sl), Write(graph1_Il), Write(graph1_Rl), run_time=3)
        self.wait(3)

        self.play(S0.animate.set_value(499999), run_time=2)
        self.wait(6)

        self.play(self.beta.animate.set_value(0.4), run_time=2)
        self.wait(6)

    def sir_model(self, t, max_t, N0, I0, beta, gamma, interval, n_type):
        global S, I, R
        name = str(N0)+"/"+str(beta)
        if name in self.list_data:
            S = self.list_data[name]["S"]
            I = self.list_data[name]["I"]
            R = self.list_data[name]["R"]
        else:
            #print(f'N0 = {str(N0)} calculating...\nt={float(max_t)}')
            ppltn_list = {
                "S": [],
                "I": [],
                "R": []
                }
            S = ppltn_list["S"]
            I = ppltn_list["I"]
            R = ppltn_list["R"]

            S.append(N0 - I0)
            I.append(I0)
            R.append(0)
            
            for i in range(0, int(max_t/interval)+1):
                dS = -beta * S[-1] * I[-1] / N0
                dI = beta * S[-1] * I[-1] / N0 - gamma * I[-1]
                dR = gamma * I[-1]
                
                S.append(max(S[-1] + round(dS,2), 0))
                I.append(min(I[-1] + round(dI,2), N0))
                R.append(max(R[-1] + round(dR,2), 0))

                if S[-1] <= 0: break

            #if S[-1]>0.0: print(f"S({t}) = {S[-1]}")
            self.list_data[name] = {"S":S, "I":I, "R":R}
            #print(f'N0 = {str(N0)} calculated. len = {str(len(S))}')

        if n_type == 'S':
            #self.St.set_value(S[ min(int(interval*float(t)), len(S)-1) ])
            #self.It.set_value(I[ min(int(interval*float(t)), len(I)-1) ])
            self.Sd.set_value(-beta * float(S[ min(int(interval*float(max_t/2))-1, len(S)-1) ]) * float(I[ min(int(interval*float(max_t/2))-1, len(I)-1) ]) / N0)
            #print(f'{str(self.St.get_value())}/{str(self.It.get_value())}')
            return (S[ min(int(interval*float(t)), len(S)-1) ])
        elif n_type == 'I': return I[ min(int(interval*float(t)), len(I)-1) ]
        elif n_type == 'R': return R[ min(int(interval*float(t)), len(R)-1) ]
        else: print('WARNING UNEXPECTED N_TYPE')

class Test2(Scene):
    def construct(self):
        axes1 = Axes(x_range=[0,10,1], y_range=[0,20,1], tips=False).add_coordinates()
        line1 = axes1.plot_line_graph(x_values=[0,5], y_values=[0,5])

        self.play(Create(axes1), Create(line1), run_time=1)
        self.wait(3)