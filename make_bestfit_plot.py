#! /usr/bin/env python

from ROOT import *
from array import array
from math import *

########################### SETTING VALUES ##############################

channel = ["Combined", "#mu#tau Non-VBF (MVA)", "#mu#tau Non-VBF (CBA)", "#mu#tau ll (MVA)", "#mu#tau VBF (CBA)", "#mu#tau VBF (MVA)"]
mu_exp = array("d", [1., 1., 1., 1., 1., 1.])
mu_obs = array("d", [0.5, 0.3, 0.1, 0.5, 0.3, 0.1])
mu_obs_stat_err = array("d", [0.1, 0.2, 0.2, 0.1, 0.2, 0.1])
mu_obs_total_err = array("d", [0.3, 0.3, 0.3, 0.3, 0.3, 0.3])
limit_obs = array("d", [0.7, 0.8, 0.85, 0.7, 0.8, 0.85])
limit_exp = array("d", [1., 1., 1., 1., 1., 1.])
limit_exp_1sigma = array("d", [0.3, 0.3, 0.3, 0.3, 0.3, 0.3])
limit_exp_2sigma = array("d", [0.6, 0.6, 0.6, 0.6, 0.6, 0.6])
signif_obs = array("d", [0.6, 0.6, 0.6, 0.6, 0.6, 0.6])
signif_exp = array("d", [0.5, 0.5, 0.5, 0.5, 0.5, 0.5])
y_line = [1, 4]
addText = True

#########################################################################


def set_canvas(x_size=800, y_size=600):
    canvas = TCanvas("", "", x_size, y_size)
    canvas.SetLeftMargin(0.25)
    canvas.SetRightMargin(0.032)
    canvas.GetFrame().SetFillColor(21)
    canvas.GetFrame().SetBorderSize(12)
    return canvas

def set_legend(x1, y1, x2, y2, text_size):
    legend = TLegend(x1, y1, x2, y2)
    legend.SetBorderSize(0)
    legend.SetFillColor(10)
    legend.SetTextSize(text_size)
    return legend

def set_label(n_channel, x_title):
    histo = TH2F("","", n_channel, -1., 3.5, n_channel+1, -0.5, n_channel)
    histo.GetYaxis().SetLabelOffset(0.04)
    histo.GetYaxis().SetNdivisions(0)
    histo.SetXTitle(x_title)
    text = TLatex()
    text.SetTextAlign(32)
    text.SetTextSize(0.03)
    return histo, text

def set_graph(n, x, e1=None, e2=None, style=None):
    y = array("d", range(n))
    zeros = array("d", [0]*n)
    if e1 is None:
        graph = TGraph(n, x, y)
    elif e2 is None:
        graph = TGraphErrors(n, x, y, e1, zeros)
    else:
        graph = TGraphAsymmErrors(n, x, y, e1, zeros, e2, zeros)
    if style is None:
        style = array("d", [0]*5)
    graph.SetLineColor(style[0])
    graph.SetLineWidth(style[1])
    graph.SetMarkerColor(style[2])
    graph.SetMarkerSize(style[3])
    graph.SetMarkerStyle(style[4])
    return graph

def main():
    gROOT.SetBatch(True)
    gStyle.SetOptStat(0)
    n_channel = len(channel)
    c = set_canvas()
    h, t = set_label(n_channel, "Branching fraction of H #rightarrow l#tau (%)")
    h.Draw()
    exp_limit = set_graph(n_channel, limit_exp, style=[0,0,1,2.7,21])
    exp_limit_1sigma = set_graph(n_channel, limit_exp, limit_exp_1sigma, style=[3,20,0,0,0])
    exp_limit_2sigma = set_graph(n_channel, limit_exp, limit_exp_2sigma, style=[5,20,0,0,0])
    obs_limit = set_graph(n_channel, limit_obs, style=[0,0,1,2.6,5])
    obs_mu = set_graph(n_channel, mu_obs, style=[0,0,1,2,8])
    obs_mu_stat = set_graph(n_channel, mu_obs, mu_obs_stat_err, style=[2,2,0,0,0])
    obs_mu_total = set_graph(n_channel, mu_obs, mu_obs_total_err, style=[4,2,0,0,0])
    gr = TMultiGraph()
    gr.Add(exp_limit_2sigma)
    gr.Add(exp_limit_1sigma)
    gr.Add(exp_limit)
    gr.Add(obs_limit)
    gr.Add(obs_mu_total)
    gr.Add(obs_mu_stat)
    gr.Add(obs_mu)
    gr.Draw("pz")
    l = TLine()
    l.SetLineStyle(2)
    l.DrawLine(0, -0.5, 0, n_channel)
    for i in y_line:
        l.DrawLine(-1, i-0.5, 3.5, i-0.5)
    leg = set_legend(0.8, 0.4, 0.95, 0.8, 0.03)
    leg.AddEntry(exp_limit, "Exp UL", "p")
    leg.AddEntry(exp_limit_1sigma, "68% Exp", "l")
    leg.AddEntry(exp_limit_2sigma, "95% Exp", "l")
    leg.AddEntry(obs_limit, "Obs UL", "p")
    leg.AddEntry(obs_mu, "Best Fit", "p")
    leg.AddEntry(obs_mu_stat, "Stat Error", "l")
    leg.AddEntry(obs_mu_total, "Total Error", "l")
    leg.Draw()
    for i,label in enumerate(channel):
        t.DrawLatex(-1.1,i,label)
    if addText:
        t.SetTextSize(0.02)
        for i in range(n_channel):
            mu_obs_syst_err = sqrt(mu_obs_total_err[i]*mu_obs_total_err[i] - mu_obs_stat_err[i]*mu_obs_stat_err[i])
            s = "#mu = %.2f #pm %.2f (%.2f(stat) #pm %.2f(syst)); Signif: Obs = %.2f, Exp = %.2f"%(mu_obs[i], mu_obs_total_err[i], mu_obs_stat_err[i], mu_obs_syst_err, signif_obs[i], signif_exp[i])
            t.DrawLatex(1.9,i+0.3,s)
            s = "UL: Obs = %.2f, Exp = %.2f #pm %.2f"%(limit_obs[i], limit_exp[i], limit_exp_1sigma[i])
            t.DrawLatex(mu_exp[i]+0.8,i-0.3,s)
    t.SetTextSize(0.05)
    t.DrawLatex(3.3,n_channel-0.3,"ATLAS Preliminary")
    c.SaveAs("results.pdf")


if __name__ == "__main__":
    main()

