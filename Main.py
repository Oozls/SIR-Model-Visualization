# -*- coding: UTF-8 -*-
from manim import *
import math

# manim ./Main.py CLASSNAME -pqm

class Test(Scene):
    def construct(self):
        self.list_data = {}

        self.S0 = 999999
        self.I0 = 1
        self.R0 = 0
        self.N0 = 1000000
        self.beta = ValueTracker(0.25)
        self.gamma = ValueTracker(0.05)

        self.dSt = ValueTracker(0)
        self.dIt = ValueTracker(0)
        self.dRt = ValueTracker(0)
        
        #PLOTS
        width1 = 240.0

        axes1 = Axes(
            x_range=[0, width1, width1/5],
            y_range=[0, 1000000, 250000],
            x_length=5.5,
            tips=False).shift(LEFT*0.5, DOWN*0.125)
        axes1.add_coordinates()
        axes1_labels = axes1.get_axis_labels(x_label="t", y_label="S")

        N1_interval = 1

        graph1_S = always_redraw(lambda: axes1.plot(
            lambda x: self.sir_model(x, width1, N1_interval, "S"),
            x_range=[0, width1, N1_interval],
            use_smoothing=False,
            color=YELLOW))
        graph1_Sl = always_redraw(lambda: axes1.get_graph_label(graph=graph1_S,
                                        label=MathTex(r"S", font_size=50),
                                        x_val=width1,
                                        direction=UP*0.5,
                                        color=YELLOW))

        graph1_I = always_redraw(lambda: axes1.plot(
            lambda x: self.sir_model(x, width1, N1_interval, "I"),
            x_range=[0, width1, N1_interval],
            use_smoothing=False,
            color=GREEN))
        graph1_Il = always_redraw(lambda: axes1.get_graph_label(graph=graph1_I,
                                        label=MathTex(r"I", font_size=50),
                                        x_val=width1*0.95,
                                        direction=UP*0.5,
                                        color=GREEN))

        graph1_R = always_redraw(lambda: axes1.plot(
            lambda x: self.sir_model(x, width1, N1_interval, "R"),
            x_range=[0, width1, N1_interval],
            use_smoothing=False,
            color=BLUE))
        graph1_Rl = always_redraw(lambda: axes1.get_graph_label(graph=graph1_R,
                                        label=MathTex(r"R", font_size=50),
                                        x_val=width1,
                                        color=BLUE))
        
        #print(np.around(np.concatenate((axes1.point_to_coords(np.array([width1/2, 100, 0])), [0]))))

        line1 = axes1.plot_line_graph(x_values=[120,120], y_values=[0,1000000], add_vertex_dots=False, line_color=RED)

        graph1_group = VGroup(axes1, graph1_S, graph1_I, graph1_R, graph1_Sl, graph1_Il, graph1_Rl, axes1_labels, line1)
        graph1_group.shift(LEFT*1.5)

        # TEXTS
        text1 = always_redraw(lambda: MathTex(r'&(t = 120)\\',
                                              r'&\frac{dS}{dt} = -\frac{\beta}{N} \cdot S \cdot I = ' + str(round(self.dSt.get_value(), 1)) + r'\\',
                                              r'&\frac{dI}{dt} = \frac{\beta}{N} \cdot S \cdot I - \gamma \cdot I = ' + str(round(self.dIt.get_value(), 1)) + r'\\',
                                              r'&\frac{dR}{dt} = \gamma \cdot I = ' + str(round(self.dRt.get_value(), 1)) + r'\\',
                                              font_size=30).to_edge(UL).shift(RIGHT*8))
        text2 = MathTex(r'&N = ' + str(round(self.N0)) + r'\\',
                        r'&S_0 = ' + str(round(self.S0)) + r'\\',
                        r'&I_0 = ' + str(round(self.I0)) + r'\\',
                        r'&R_0 = ' + str(round(self.R0)),
                        font_size=30).to_edge(UL).shift(RIGHT*8, DOWN*3)
        text3 = always_redraw(lambda: MathTex(r'&\beta = ' + str(round(self.beta.get_value(), 2)) + r'\\',
                                              r'&\gamma = ' + str(round(self.gamma.get_value(), 2)) + r'\\',
                                              font_size=30).to_edge(UL).shift(RIGHT*8, DOWN*5.25))

        '''graph2 = always_redraw(lambda: axes1.plot(
            lambda x: self.sir_model(50, S0.get_value(), 1, 1.2, 0)['S'][ min( round(x), len( self.sir_model(50, S0.get_value(), 1, 1.2, 0)['S'] )-1 ) ], 
            x_range=[0, 50, 1],
            use_smoothing=False,
            color=BLUE))
        
        graph2_group = VGroup(graph2)
        graph2_group.shift(LEFT*1.5)'''

        # PLAYING
        self.play(Write(text1), Write(text2), Write(text3), run_time=5)
        self.play(DrawBorderThenFill(axes1), Write(axes1_labels))
        self.play(Create(graph1_S), Create(graph1_I), Create(graph1_R), Create(line1), Write(graph1_Sl), Write(graph1_Il), Write(graph1_Rl), run_time=3)
        self.wait(3)

        self.play(self.beta.animate.set_value(0.4), run_time=5)
        self.wait(6)

        self.play(self.gamma.animate.set_value(0.15), run_time=5)
        self.wait(6)

    def sir_model(self, t, max_t, interval, n_type):
        global S, I, R
        name = str(self.N0)+"/"+str(round(self.beta.get_value(),2))+"/"+str(round(self.gamma.get_value(),2))
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

            S.append(self.N0 - self.I0)
            I.append(self.I0)
            R.append(self.R0)
            
            for i in range(0, int(max_t/interval)+1):
                dS = -self.beta.get_value()* S[-1] * I[-1] / self.N0
                dI = self.beta.get_value() * S[-1] * I[-1] / self.N0 - self.gamma.get_value() * I[-1]
                dR = self.gamma.get_value() * I[-1]
                
                S.append(max(S[-1] + round(dS,2), 0))
                I.append(min(I[-1] + round(dI,2), self.N0))
                R.append(max(R[-1] + round(dR,2), 0))

                if S[-1] <= 0: break

            #if S[-1]>0.0: print(f"S({t}) = {S[-1]}")
            self.list_data[name] = {"S":S, "I":I, "R":R}
            #print(f'N0 = {str(N0)} calculated. len = {str(len(S))}')

        if n_type == 'S':
            #self.St.set_value(S[ min(int(interval*float(t)), len(S)-1) ])
            #self.It.set_value(I[ min(int(interval*float(t)), len(I)-1) ])
            self.dSt.set_value(-self.beta.get_value() * float(S[ min(int(interval*float(max_t/2))-1, len(S)-1) ]) * float(I[ min(int(interval*float(max_t/2))-1, len(I)-1) ]) / self.N0)
            self.dRt.set_value(self.gamma.get_value() * float(I[ min(int(interval*float(max_t/2))-1, len(I)-1) ]))
            self.dIt.set_value(-1 * self.dSt.get_value() - self.dRt.get_value())
            #print(f'{str(self.St.get_value())}/{str(self.It.get_value())}')
            return (S[ min(int(interval*float(t)), len(S)-1) ])
        elif n_type == 'I': return I[ min(int(interval*float(t)), len(I)-1) ]
        elif n_type == 'R': return R[ min(int(interval*float(t)), len(R)-1) ]
        else: print('WARNING UNEXPECTED N_TYPE')

class Test2(Scene):
    def construct(self):
        self.list_data = {}

        self.S0 = 999999
        self.I0 = 1
        self.R0 = 0
        self.N0 = 1000000
        self.beta = ValueTracker(0.25)
        self.gamma = ValueTracker(0.05)

        self.dSt = ValueTracker(0)
        self.dIt = ValueTracker(0)
        self.dRt = ValueTracker(0)
        
        #PLOTS
        width1 = 350.0

        axes1 = Axes(
            x_range=[0, width1, width1/5],
            y_range=[0, 1000000, 250000],
            x_length=8,
            tips=False).shift(LEFT*1.5)
        axes1.add_coordinates()
        axes1_labels = axes1.get_axis_labels(x_label="t", y_label="S")

        N1_interval = 1

        graph1_S = always_redraw(lambda: axes1.plot(
            lambda x: self.sir_model(x, width1, N1_interval, "S"),
            x_range=[0, width1, N1_interval],
            use_smoothing=False,
            color=YELLOW))
        graph1_Sl = always_redraw(lambda: axes1.get_graph_label(graph=graph1_S,
                                        label=MathTex(r"S", font_size=50),
                                        x_val=width1,
                                        direction=UP*0.5,
                                        color=YELLOW))

        graph1_I = always_redraw(lambda: axes1.plot(
            lambda x: self.sir_model(x, width1, N1_interval, "I"),
            x_range=[0, width1, N1_interval],
            use_smoothing=False,
            color=GREEN))
        graph1_Il = always_redraw(lambda: axes1.get_graph_label(graph=graph1_I,
                                        label=MathTex(r"I", font_size=50),
                                        x_val=width1*0.95,
                                        direction=UP*0.5,
                                        color=GREEN))

        graph1_R = always_redraw(lambda: axes1.plot(
            lambda x: self.sir_model(x, width1, N1_interval, "R"),
            x_range=[0, width1, N1_interval],
            use_smoothing=False,
            color=BLUE))
        graph1_Rl = always_redraw(lambda: axes1.get_graph_label(graph=graph1_R,
                                        label=MathTex(r"R", font_size=50),
                                        x_val=width1,
                                        color=BLUE))
        
        #print(np.around(np.concatenate((axes1.point_to_coords(np.array([width1/2, 100, 0])), [0]))))

        #line1 = axes1.plot_line_graph(x_values=[48,48], y_values=[0,1000000], add_vertex_dots=False, line_color=RED)

        graph1_group = VGroup(axes1, graph1_S, graph1_I, graph1_R, graph1_Sl, graph1_Il, graph1_Rl, axes1_labels)
        graph1_group.shift(LEFT*1.5)

        # TEXTS
        '''text1 = always_redraw(lambda: MathTex(r'&(when t = 120)\\',
                                              r'&\frac{dS}{dt} = -\frac{\beta}{N} \cdot S \cdot I = ' + str(round(self.dSt.get_value(), 1)) + r'\\',
                                              r'&\frac{dI}{dt} = \frac{\beta}{N} \cdot S \cdot I - \gamma \cdot I = ' + str(round(self.dIt.get_value(), 1)) + r'\\',
                                              r'&\frac{dR}{dt} = \gamma \cdot I = ' + str(round(self.dRt.get_value(), 1)) + r'\\',
                                              font_size=30).to_edge(UL).shift(RIGHT*8))
        text2 = MathTex(r'&N = ' + str(round(self.N0)) + r'\\',
                        r'&S_0 = ' + str(round(self.S0)) + r'\\',
                        r'&I_0 = ' + str(round(self.I0)) + r'\\',
                        r'&R_0 = ' + str(round(self.R0)),
                        font_size=30).to_edge(UL).shift(RIGHT*8, DOWN*3)
        text3 = always_redraw(lambda: MathTex(r'&\beta = ' + str(round(self.beta.get_value(), 2)) + r'\\',
                                              r'&\gamma = ' + str(round(self.gamma.get_value(), 2)) + r'\\',
                                              font_size=30).to_edge(UL).shift(RIGHT*8, DOWN*6))'''

        '''graph2 = always_redraw(lambda: axes1.plot(
            lambda x: self.sir_model(50, S0.get_value(), 1, 1.2, 0)['S'][ min( round(x), len( self.sir_model(50, S0.get_value(), 1, 1.2, 0)['S'] )-1 ) ], 
            x_range=[0, 50, 1],
            use_smoothing=False,
            color=BLUE))
        
        graph2_group = VGroup(graph2)
        graph2_group.shift(LEFT*1.5)'''

        # PLAYING
        #self.play(Write(text1), Write(text2), Write(text3), run_time=5)
        self.play(DrawBorderThenFill(axes1), Write(axes1_labels))
        self.play(Create(graph1_S), Create(graph1_I), Create(graph1_R), Write(graph1_Sl), Write(graph1_Il), Write(graph1_Rl), run_time=3)
        self.wait(3)

        '''self.play(self.beta.animate.set_value(0.4), run_time=5)
        self.wait(6)

        self.play(self.gamma.animate.set_value(0.15), run_time=5)
        self.wait(6)'''

    def sir_model(self, t, max_t, interval, n_type):
        global S, I, R

        name = str(self.N0)
        if name in self.list_data:
            S = self.list_data[name]["S"]
            I = self.list_data[name]["I"]
            R = self.list_data[name]["R"]
        else:
            #print(f'N0 = {str(N0)} calculating...\nt={float(max_t)}')
            reprod = [
                1.5, 0.81, 9.35, 5.66, 1.94, 0.67, 0.45, 0.76, 0.85, 0.67,
                0.53, 0.58, 0.59, 0.75, 4.58, 0.84, 1.52, 1.30, 1.11, 0.91,
                0.88, 1.11, 1.00, 0.70, 1.05, 0.89, 0.84, 1.93, 3.05, 1.38,
                0.90, 0.68, 0.82, 0.82, 0.81, 0.97, 1.00, 1.06, 1.17, 1.05,
                1.12, 1.52, 1.43, 1.23, 1.18, 1.28, 1.11, 1.00, 0.88, 0.79
            ]
            gamma = 0.15
            beta_list = []
            gamma_list = []
            for i in reprod:
                # gamma * r0 = beta
                # (r0 + 1) * gamma = 1
                # gamma = 1 / (r0 + 1)
                gamma_list.append(4 / (i + 1))
                beta_list.append(i * (4 / (i + 1)))
            print(beta_list)
            print(gamma_list)

            ppltn_list = {
                "S": [],
                "I": [],
                "R": []
                }
            S = ppltn_list["S"]
            I = ppltn_list["I"]
            R = ppltn_list["R"]

            S.append(self.N0 - self.I0)
            I.append(self.I0)
            R.append(self.R0)
            
            for i in range(0, int(max_t/interval)+1):
                #print(str(beta_list[max(int(i/7)-1, 0)]))
                dS = -beta_list[max(int(i/7)-1, 0)] * S[-1] * I[-1] / self.N0
                dI = beta_list[max(int(i/7)-1, 0)] * S[-1] * I[-1] / self.N0 - gamma_list[max(int(i/7)-1, 0)] * I[-1]
                dR = gamma_list[max(int(i/7)-1, 0)] * I[-1]
                
                S.append(max(S[-1] + round(dS,2), 0))
                I.append(min(I[-1] + round(dI,2), self.N0))
                R.append(max(R[-1] + round(dR,2), 0))

                if S[-1] <= 0: break

            #if S[-1]>0.0: print(f"S({t}) = {S[-1]}")
            self.list_data[name] = {"S":S, "I":I, "R":R}
            #print(f'N0 = {str(N0)} calculated. len = {str(len(S))}')

        if n_type == 'S':
            #self.St.set_value(S[ min(int(interval*float(t)), len(S)-1) ])
            #self.It.set_value(I[ min(int(interval*float(t)), len(I)-1) ])
            '''self.dSt.set_value(-self.beta.get_value() * float(S[ min(int(interval*float(max_t/2))-1, len(S)-1) ]) * float(I[ min(int(interval*float(max_t/2))-1, len(I)-1) ]) / self.N0)
            self.dRt.set_value(self.gamma.get_value() * float(I[ min(int(interval*float(max_t/2))-1, len(I)-1) ]))
            self.dIt.set_value(-1 * self.dSt.get_value() - self.dRt.get_value())'''
            #print(f'{str(self.St.get_value())}/{str(self.It.get_value())}')
            return (S[ min(int(interval*float(t)), len(S)-1) ])
        elif n_type == 'I': return I[ min(int(interval*float(t)), len(I)-1) ]
        elif n_type == 'R': return R[ min(int(interval*float(t)), len(R)-1) ]
        else: print('WARNING UNEXPECTED N_TYPE')