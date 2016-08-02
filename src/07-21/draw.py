__author__ = 'amrit'

import matplotlib.pyplot as plt
import os, pickle
import operator
import numpy as np
import matplotlib.cm as cmx
import matplotlib.colors as colors

if __name__ == '__main__':
    '''F_final = {}
    F_final1={}
    fileB = ['pitsA', 'pitsB', 'pitsC', 'pitsD', 'pitsE', 'pitsF']
    path = '/home/amrit/GITHUB/Pits_lda/src/07-21/dump/baseline'
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            a = os.path.join(root, name)
            with open(a, 'rb') as handle:
                F_final = {}
                F_final = pickle.load(handle)
                # print(F_final)
                F_final1 = dict(F_final1.items() + F_final.items())
    print(F_final1)'''
    de={'SE0': {'tf': {'no_shingle': [0.63574660633484159, 0.61846496106785309, 0.63666300768386386, 0.66971428571428571, 0.62940461725394892, 0.60591133004926101, 0.63041065482796887, 0.63519313304721026, 0.64961067853170185, 0.64538198403648805, 0.63625450180072018, 0.65494505494505506, 0.62053056516724325, 0.61899179366940216, 0.62597114317425073, 0.65297297297297296, 0.59106529209622005, 0.65893271461716929, 0.64388092613009928, 0.61538461538461542, 0.59999999999999998, 0.6289445048966269, 0.65207877461706787, 0.65315852205005975, 0.61865407319952781]}}, 'SE6': {'tf': {'no_shingle': [0.71203703703703713, 0.71395240317312192, 0.69405099150141636, 0.67902439024390238, 0.70460959548447788, 0.72065514103730666, 0.72091954022988514, 0.69586614173228345, 0.70571563533301851, 0.69990680335507927, 0.70986183897093846, 0.70415879017013228, 0.73157415832575057, 0.71166827386692377, 0.71144749290444653, 0.70047393364928923, 0.70764899108399804, 0.72064393939393945, 0.72549019607843135, 0.71374407582938393, 0.7000481463649495, 0.69623655913978488, 0.70992007522331924, 0.71265461465271185, 0.71516296646197453]}}, 'SE3': {'tf': {'no_shingle': [0.71525688175638014, 0.71689242135900588, 0.70441501103752768, 0.71296086858176877, 0.71097615834457939, 0.71479342514438016, 0.70730103047577286, 0.70949477351916368, 0.71552014364268868, 0.71248724055801294, 0.711378044711378, 0.7164570803717879, 0.71265678449258829, 0.71239688100350307, 0.72342793544796902, 0.72211803640375072, 0.71541988147154201, 0.71999999999999986, 0.72036541889483063, 0.71029529130087787, 0.70618789521228553, 0.71335284845755453, 0.71667602470522174, 0.70992028343666969, 0.71018334437817532]}}, 'SE1': {'tf': {'no_shingle': [0.99970451070827504, 0.99970450311556491, 0.99978160048304832, 0.99973020542929447, 0.99978160048304832, 0.9997944607163044, 0.99973020542929447, 0.99978160048304832, 0.99980730444612875, 0.99974304948866854, 0.99961454452010801, 0.99973020542929447, 0.99974304948866854, 0.99979445543536904, 0.99978160048304832, 0.99976876236479018, 0.99970450311556491, 0.99978160048304832, 0.99964024155210074, 0.99980729949512459, 0.99975591269382458, 0.99976875642343255, 0.99970449552246476, 0.99980730444612875, 0.99970449552246476]}}, 'SE8': {'tf': {'no_shingle': [0.70755704416998133, 0.70930726731831695, 0.71401554948518597, 0.7145448724789244, 0.71131447587354413, 0.71154863977982419, 0.72390285470813809, 0.71744419760922462, 0.70135557872784149, 0.71222866967547804, 0.71731374606505771, 0.71895013123359575, 0.71277271764456684, 0.71152621524092552, 0.72072265835036031, 0.71924290220820186, 0.71518987341772156, 0.70351652979574641, 0.71027244778967458, 0.71804590440092653, 0.70623328533223617, 0.71150139216106234, 0.71920364993778507, 0.72076677316293924, 0.71836476662100934]}}}
    untuned={'SE6': {'tf': {'no_shingle': [0.86479638009049775, 0.86834937352460506, 0.86828201858261977, 0.8615497612926919, 0.86920138257231205, 0.8669790915645279, 0.85811781609195403, 0.87230514096185752, 0.86258005489478495, 0.86255924170616127, 0.86463039942165199, 0.85916258836324089, 0.86887321396274186, 0.86276653909240031, 0.87018181818181817, 0.87590448625180894, 0.86881410833183381, 0.85777777777777775, 0.86556902478740727, 0.86980207009260946, 0.86010928961748634, 0.8742104313300848, 0.86623282718727401, 0.86426085363619709, 0.86338002546843728]}}, 'SE8': {'tf': {'no_shingle': [0.67484874675885909, 0.69146238377007618, 0.69016949152542384, 0.69501863774991535, 0.68264878457669742, 0.69039145907473309, 0.69036388140161731, 0.68613387978142071, 0.68626110731373891, 0.68470588235294116, 0.6893106893106894, 0.69012178619756437, 0.68500170823368645, 0.68754301445285626, 0.68997271487039558, 0.6887099537433613, 0.69060402684563749, 0.68884339815762541, 0.67937257547647167, 0.69128658951667799, 0.68226974238087224, 0.68468776732249781, 0.68074238038481183, 0.67546084897683079, 0.67640067911714774]}}, 'SE3': {'tf': {'no_shingle': [0.78554514568104605, 0.79282455412691832, 0.78438818565400836, 0.78920389162046223, 0.78935837245696405, 0.79225061830173127, 0.78138551031200421, 0.79048014965703606, 0.79352977539666192, 0.79185101347875286, 0.78589889382818146, 0.79688322628198371, 0.78860693940963245, 0.77755553216128015, 0.78951201747997091, 0.7917568263781557, 0.78866296980899564, 0.78506622171237883, 0.79056721379596917, 0.79481865284974085, 0.78706311945748553, 0.78675936494759791, 0.78725182863113896, 0.79105867742936975, 0.7871101871101871]}}, 'SE1': {'tf': {'no_shingle': [0.68088574921885614, 0.68133351329464165, 0.68098905553303601, 0.68513439385628083, 0.68835200431907129, 0.68120572301708571, 0.67740174672489084, 0.69620075704472173, 0.68894040638210818, 0.68500687757909218, 0.69046021736213603, 0.68752584424534802, 0.68624504849064327, 0.69948831420273816, 0.67880613362541076, 0.68330394683303941, 0.66910569105691065, 0.67180735930735935, 0.6831911147230123, 0.68622837370242218, 0.6794678370593884, 0.69243113131853429, 0.68422511782644868, 0.67143840330351001, 0.68007662835249039]}}, 'SE0': {'tf': {'no_shingle': [0.73112208892025399, 0.74309978768577478, 0.73279052553663959, 0.73712737127371275, 0.7436582109479305, 0.73440784863349684, 0.69546120058565153, 0.70579603815113712, 0.72919605077574046, 0.75862068965517249, 0.72944693572496266, 0.73990077958894407, 0.73387694588584151, 0.7491361437456806, 0.71637426900584789, 0.70990734141126166, 0.72401433691756267, 0.72816901408450707, 0.75070422535211279, 0.73049645390070927, 0.71590909090909094, 0.72059925093632948, 0.74491180461329709, 0.72065888812628687, 0.72638888888888897]}}}
    baseline={'SE6': {'tf': {'no_shingle': [0.64255910987482623, 0.65229110512129374, 0.65368567454798332, 0.66086956521739137, 0.66180758017492713, 0.6696562032884904, 0.6384180790960452, 0.6370597243491577, 0.64535768645357683, 0.70541611624834866, 0.62446043165467624, 0.66850828729281775, 0.63492063492063489, 0.63173216885007277, 0.67219917012448138, 0.6831275720164609, 0.61849710982658956, 0.63142857142857145, 0.64722222222222214, 0.62551440329218111, 0.6574202496532594, 0.61731843575418988, 0.66666666666666674, 0.64347826086956517, 0.65101721439749605]}}, 'SE0': {'tf': {'no_shingle': [0.65740740740740744, 0.67126436781609189, 0.71367521367521369, 0.69281045751633985, 0.70207852193995379, 0.67720090293453727, 0.72768878718535468, 0.70535714285714279, 0.70852017937219725, 0.69506726457399115, 0.74509803921568629, 0.73008849557522115, 0.65759637188208619, 0.74042553191489369, 0.72429906542056066, 0.73043478260869554, 0.72197309417040356, 0.69461077844311381, 0.65048543689320393, 0.71264367816091956, 0.70069605568445481, 0.72258064516129028, 0.71964679911699769, 0.72151898734177211, 0.69425287356321841]}}, 'SE3': {'tf': {'no_shingle': [0.44286979627989376, 0.39461883408071746, 0.45484949832775923, 0.4403361344537815, 0.41373239436619719, 0.45873153779322329, 0.43589743589743585, 0.3996415770609319, 0.42832764505119458, 0.39677419354838717, 0.42154566744730682, 0.41129744042365401, 0.43330501274426508, 0.4637404580152672, 0.43321299638989164, 0.4274265360641139, 0.39966694421315563, 0.41459074733096085, 0.42680776014109351, 0.44127516778523496, 0.40669456066945608, 0.38793103448275862, 0.42932862190812726, 0.42907180385288973, 0.41506129597197899]}}, 'SE1': {'tf': {'no_shingle': [0.67248545303408158, 0.6875773834089971, 0.67334167709637049, 0.64333333333333342, 0.66032843560933452, 0.67340918668352301, 0.68139337298215796, 0.64885177453027143, 0.66916666666666658, 0.65953067105804852, 0.67573310667233311, 0.64231738035264474, 0.65866776996276377, 0.64009962640099616, 0.6775911511675542, 0.65772357723577235, 0.67581047381546133, 0.689308176100629, 0.67195767195767209, 0.67584480600750929, 0.67450650986980254, 0.68097643097643101, 0.65976714100905565, 0.68010291595197248, 0.65698587127158548]}}, 'SE8': {'tf': {'no_shingle': [0.47588424437299032, 0.35862068965517241, 0.40894568690095845, 0.40845070422535212, 0.38271604938271608, 0.44444444444444442, 0.4157706093189964, 0.3848580441640379, 0.48192771084337344, 0.33793103448275857, 0.34267912772585668, 0.37308868501529052, 0.40531561461794019, 0.45205479452054792, 0.40125391849529779, 0.39597315436241615, 0.40000000000000002, 0.43887147335423199, 0.45859872611464969, 0.34951456310679618, 0.39528023598820061, 0.44604316546762585, 0.42384105960264901, 0.40549828178694153, 0.33444816053511706]}}}

    fileB = ['SE0', 'SE6', 'SE3', 'SE8', 'SE1']
    #labels = [1, 2, 3, 4, 5, 6, 7, 8, 9]


    temp=[]
    temp1=[]
    temp2=[]
    temp3=[]
    temp4=[]
    temp5=[]
    for file in fileB:
        temp.append(np.median(de[file]['tf']['no_shingle']))
        temp1.append(np.median(baseline[file]['tf']['no_shingle']))
        temp2.append(np.median(untuned[file]['tf']['no_shingle']))

        temp3.append(np.percentile(de[file]['tf']['no_shingle'],75)-np.percentile(de[file]['tf']['no_shingle'],25))
        temp4.append(np.percentile(baseline[file]['tf']['no_shingle'],75)-np.percentile(baseline[file]['tf']['no_shingle'],25))
        temp5.append(np.percentile(untuned[file]['tf']['no_shingle'],75)-np.percentile(untuned[file]['tf']['no_shingle'],25))
    median={}
    median['baseline']=temp1
    median['untuned']=temp2
    median['tuned']=temp
    iqr={}
    iqr['baseline']=temp4
    iqr['untuned']=temp5
    iqr['tuned']=temp3
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 70}

    plt.rc('font', **font)
    paras={'lines.linewidth': 8,'legend.fontsize': 60, 'axes.labelsize': 70, 'legend.frameon': False,'figure.autolayout': True,'figure.figsize': (16,8)}
    plt.rcParams.update(paras)
    X = range(len(fileB))
    plt.figure(num=0, figsize=(40, 25))
    #plt.subplot(121)
    results=['baseline','untuned','tuned']
    for res in results:
        line, = plt.plot(X, median[res], marker='o', markersize=16, label=res+'_median')
        plt.plot(X, iqr[res], linestyle="-.", color=line.get_color(), marker='*', markersize=16, label=res + '_iqr')


    #plt.ylim(-0.1,1.1)

    plt.xticks(X, fileB)
    plt.ylabel("F_score")
    plt.xlabel("Datasets")
    plt.legend(bbox_to_anchor=(0.3, 0.8), loc=1, ncol = 1, borderaxespad=0.)
    plt.savefig("graph" + ".png")