#!/usr/b973675687568in/env python

import pyodbc
import json
import sys
from os import popen,environ

DSN = sys.argv[1]
key = ["{#TBSPNAME}"]
CRED = {

	'KS3056U':{
                'user':'ZABBIX',
                'password':'PEWPEWPEWhandsup2'
                },

	'KS4551':{
                'user':'ZABBIX',
                'password':'PEWPEWPEWhandsup1'
                },

	'KS2350':{
                'user':'ZABBIX',
                'password':'P2544734515'
                },

	'KS2357':{
                'user':'ZABBIX',
                'password':'P2633706298'
                },
	
	'KS2364':{
                'user':'ZABBIX',
                'password':'P2554134302'
                },

	'KS2370':{
                'user':'ZABBIX',
                'password':'P2584402114'
                },
	
	'KS2374':{
                'user':'ZABBIX',
                'password':'P2584461080'
                },
	
	'KS2375':{
                'user':'ZABBIX',
                'password':'P2695998660'
                },
	
	'KS2378':{
                'user':'ZABBIX',
                'password':'P2539619948'
                },

	'KS2380':{
                'user':'ZABBIX',
                'password':'P2575330101'
                },
	
	'KS2384':{
                'user':'ZABBIX',
                'password':'P2528821310'
                },

	'KS2390':{
                'user':'ZABBIX',
                'password':'P2569074286'
                },

	'KS2450':{
                'user':'ZABBIX',
                'password':'P2555551508'
                },
	
	'KS2452':{
                'user':'ZABBIX',
                'password':'P2546875892'
                },

	'KS2455':{
                'user':'ZABBIX',
                'password':'P2539543715'
                },
	
	'KS2457':{
                'user':'ZABBIX',
                'password':'P2605533267'
                },
	
	'KS2464':{
                'user':'ZABBIX',
                'password':'P2633706298'
                },

	'KS2465':{
                'user':'ZABBIX',
                'password':'P2633706298'
                },

	'KS2466':{
                'user':'ZABBIX',
                'password':'P2633706298'
                },

	'KS2467':{
                'user':'ZABBIX',
                'password':'P2567453071'
                },
	
	'KS2469':{
                'user':'ZABBIX',
                'password':'P2566593014'
                },
	
	
	'KS2471':{
                'user':'ZABBIX',
                'password':'P2566065495'
                },

	'KS2474':{
                'user':'ZABBIX',
                'password':'P2532914936'
                },
	
	'KS2475':{
                'user':'ZABBIX',
                'password':'P2545158872'
                },
	
	'KS2483':{
                'user':'ZABBIX',
                'password':'P2531155885'
                },

	'KS2485':{
                'user':'ZABBIX',
                'password':'P2568388675'
                },

	'KS2486':{
                'user':'ZABBIX',
                'password':'P2565396014'
                },

	'KS2487':{
                'user':'ZABBIX',
                'password':'P2607363668'
                },
	
	
	'KS2489':{
                'user':'ZABBIX',
                'password':'P2607355033'
                },

	'KS2490':{
                'user':'ZABBIX',
                'password':'P2607351729'
                },


	'KS2492':{
                'user':'ZABBIX',
                'password':'P2633706298'
                },

	'KS2493':{
                'user':'ZABBIX',
                'password':'P2633706298'
                },

	'KS2495':{
                'user':'ZABBIX',
                'password':'P2797714470'
                },

	'KS2500':{
                'user':'ZABBIX',
                'password':'P2565799002'
                },

	'KS2501':{
                'user':'ZABBIX',
                'password':'P2535123063'
                },


	'KS2503':{
                'user':'ZABBIX',
                'password':'P2527695225'
                },

	'KS2504':{
                'user':'ZABBIX',
                'password':'P2633706298'
                },

	'KS2505':{
                'user':'ZABBIX',
                'password':'P2565810006'
                },


	'KS2507':{
                'user':'ZABBIX',
                'password':'P2531583910'
                },

	'KS2512':{
                'user':'ZABBIX',
                'password':'P2535713464'
                },


	'KS2514':{
                'user':'ZABBIX',
                'password':'P2527103132'
                },

	'KS2520':{
                'user':'ZABBIX',
                'password':'P2549901697'
                },



	'KS2521':{
                'user':'ZABBIX',
                'password':'P2536449766'
                },

	'KS2524':{
                'user':'ZABBIX',
                'password':'P2528297291'
                },

	'KS2525':{
                'user':'ZABBIX',
                'password':'P2528753704'
                },

	'KS2526':{
                'user':'ZABBIX',
                'password':'P2528749282'
                },

	'KS2527':{
                'user':'ZABBIX',
                'password':'P2538423751'
                },

	'KS2528':{
                'user':'ZABBIX',
                'password':'P2538678774'
                },


	'KS2529':{
                'user':'ZABBIX',
                'password':'P2539394251'
                },

	'KS2530':{
                'user':'ZABBIX',
                'password':'P2537540938'
                },


	'KS2532':{
                'user':'ZABBIX',
                'password':'P2539625789'
                },

	'KS2533':{
                'user':'ZABBIX',
                'password':'P2539627608'
                },

	'KS2534':{
                'user':'ZABBIX',
                'password':'P2546284700'
                },


	'KS2535':{
                'user':'ZABBIX',
                'password':'P2633706298'
                },

	'KS2536':{
                'user':'ZABBIX',
                'password':'P2676301927'
                },

	'KS2538':{
                'user':'ZABBIX',
                'password':'P2675537418'
                },

	'KS4551':{
                'user':'ZABBIX',
                'password':'P2567774343'
                },

	'KS4552':{
                'user':'ZABBIX',
                'password':'P2560092074'
                },


	'KS4555':{
                'user':'ZABBIX',
                'password':'P2562795134'
                },


	'KS4557':{
                'user':'ZABBIX',
                'password':'P2565288000'
                },

	'KS4559':{
                'user':'ZABBIX',
                'password':'P2565556930'
                },

	'KS4560':{
                'user':'ZABBIX',
                'password':'P2557234170'
                },

	'KS4561':{
                'user':'ZABBIX',
                'password':'P2559220620'
                },

	
	'KS4565':{
                'user':'ZABBIX',
                'password':'P2559663246'
                },

	'KS4566':{
                'user':'ZABBIX',
                'password':'P2558455148'
                },

	'KS4568':{
                'user':'ZABBIX',
                'password':'P2564265808'
                },


	'KS4569':{
                'user':'ZABBIX',
                'password':'P2558031670'
                },

	'KS4570':{
                'user':'ZABBIX',
                'password':'P2561836745'
                },

	
	'KS4573':{
                'user':'ZABBIX',
                'password':'P2554825723'
                },

	'KS4574':{
                'user':'ZABBIX',
                'password':'P2555355149'
                },

	'KS4576':{
                'user':'ZABBIX',
                'password':'P2535839002'
                },


	'KS4584':{
                'user':'ZABBIX',
                'password':'P2609689053'
                },

	'KS4587':{
                'user':'ZABBIX',
                'password':'P2569573280'
                },

	'KS4588':{
                'user':'ZABBIX',
                'password':'P2584822598'
                },

	'KS4595':{
                'user':'ZABBIX',
                'password':'P2741030419'
                },
                
        'KS4609':{
                'user':'ZABBIX',
                'password':'P2554644842'
                },
                
        
        'KS4611':{
                'user':'ZABBIX',
                'password':'P2560873191'
                },
                
        'KS4612':{
                'user':'ZABBIX',
                'password':'P2551878205'
                },
                
        'KS4613':{
                'user':'ZABBIX',
                'password':'P2551814254'
                },
                
        'KS4615':{
                'user':'ZABBIX',
                'password':'P2564748614'
                },
                
        'KS4617':{
                'user':'ZABBIX',
                'password':'P2626450914'
                },
                
        'KS4618':{
                'user':'ZABBIX',
                'password':'P2701646178'
                },
                
        'KS4624':{
                'user':'ZABBIX',
                'password':'P2567448911'
                },
                
        'KS4625':{
                'user':'ZABBIX',
                'password':'P2570387133'
                },
        'KS4626':{
                'user':'ZABBIX',
                'password':'P2563031366'
                },
                
        'KS4629':{
                'user':'ZABBIX',
                'password':'P2557670657'
                },
                
        'KS4631':{
                'user':'ZABBIX',
                'password':'P2559749274'
                },
        'KS4632':{
                'user':'ZABBIX',
                'password':'P2569774794'
                },
                
                
        'KS4636':{
                'user':'ZABBIX',
                'password':'P2565406134'
                },
                
                
        'KS4640':{
                'user':'ZABBIX',
                'password':'P2573509313'
                },
                
        'KS4646':{
                'user':'ZABBIX',
                'password':'P2533318888'
                },
                
	'KS4648':{
                'user':'ZABBIX',
                'password':'P2547321852'
                },
                
        'KS4650':{
                'user':'ZABBIX',
                'password':'P2569598688'
                },
                
        'KS4654':{
                'user':'ZABBIX',
                'password':'P2568395393'
                },
                
        'KS4657':{
                'user':'ZABBIX',
                'password':'P2587233865'
                },
                
        'KS4659':{
                'user':'ZABBIX',
                'password':'P2589641763'
                },
                
        'KS4662':{
                'user':'ZABBIX',
                'password':'P2569960647'
                },
                
        'KS4663':{
                'user':'ZABBIX',
                'password':'P2558115605'
                },
                
        'KS4664':{
                'user':'ZABBIX',
                'password':'P2559245532'
                },
                
        'KS4665':{
                'user':'ZABBIX',
                'password':'P2559487633'
                },
                
                
        'KS4668':{
                'user':'ZABBIX',
                'password':'P2534038531'
                },
                
        'KS4669':{
                'user':'ZABBIX',
                'password':'P2554929620'
                },
                
        'KS4670':{
                'user':'ZABBIX',
                'password':'P2557179019'
                },
                
        'KS4673':{
                'user':'ZABBIX',
                'password':'P2529597060'
                },
                
        'KS4676':{
                'user':'ZABBIX',
                'password':'P2549202371'
                },
                
        'KS4678':{
                'user':'ZABBIX',
                'password':'P2568838005'
                },
                
        'KS5100':{
                'user':'ZABBIX',
                'password':'P2558649167'
                },
                
        'KS5105':{
                'user':'ZABBIX',
                'password':'P2551538338'
                },
                
        'KS5106':{
                'user':'ZABBIX',
                'password':'P2534528936'
                },
                
        'KS5109':{
                'user':'ZABBIX',
                'password':'P2602419963'
                },
                
                
        'KS5115':{
                'user':'ZABBIX',
                'password':'P2612838912'
                },
                
        'KS5116':{
                'user':'ZABBIX',
                'password':'P2612910582'
                },
                
        'KS5117':{
                'user':'ZABBIX',
                'password':'P2612891716'
                },
                
        'KS5118':{
                'user':'ZABBIX',
                'password':'P2623360142'
                },
                
        'KS5119':{
                'user':'ZABBIX',
                'password':'P2659811414'
                },
                
        'KS5120':{
                'user':'ZABBIX',
                'password':'P2633706298'
                },
                
        'KS5121':{
                'user':'ZABBIX',
                'password':'P2633706298'
                },
                
        'KS5122':{
                'user':'ZABBIX',
                'password':'P2567219094'
                },
                
        'KS5123':{
                'user':'ZABBIX',
                'password':'P2568664967'
                },
                
        'KS5124':{
                'user':'ZABBIX',
                'password':'P2539894088'
                },
                
        'KS5126':{
                'user':'ZABBIX',
                'password':'P2564579452'
                },
                
        'KS5127':{
                'user':'ZABBIX',
                'password':'P2567957584'
                },
                
        'KS5128':{
                'user':'ZABBIX',
                'password':'P2568041551'
                },
                
        'KS5129':{
                'user':'ZABBIX',
                'password':'P2565974576'
                },
                
        'KS5130':{
                'user':'ZABBIX',
                'password':'P2537992793'
                },
                
        'KS5131':{
                'user':'ZABBIX',
                'password':'P2553457419'
                },
                
        'KS5132':{
                'user':'ZABBIX',
                'password':'P2537980762'
                },
                
        'KS5133':{
                'user':'ZABBIX',
                'password':'P2538060984'
                },
                
        'KS5134':{
                'user':'ZABBIX',
                'password':'P2537837941'
                },
                
        'KS5135':{
                'user':'ZABBIX',
                'password':'P2565388395'
                },
                
        'KS5139':{
                'user':'ZABBIX',
                'password':'P2633706298'
                },
                
        'KS5140':{
                'user':'ZABBIX',
                'password':'P2541521923'
                },
                
        'KS5141':{
                'user':'ZABBIX',
                'password':'P2800462979'
                },
                
        'KS5142':{
                'user':'ZABBIX',
                'password':'P2611365367'
                },
                
        'KS5143':{
                'user':'ZABBIX',
                'password':'P2800464649'
                },
                
        'KS7450':{
                'user':'ZABBIX',
                'password':'P2539280033'
                },
                
        'KS7451':{
                'user':'ZABBIX',
                'password':'P2528919518'
                },
                
        'KS7452':{
                'user':'ZABBIX',
                'password':'P2723841449'
                },
                
        'KS7453':{
                'user':'ZABBIX',
                'password':'P2544459455'
                },
                
                
        'KS7455':{
                'user':'ZABBIX',
                'password':'P2633706298'
                },
                
        'KS7456':{
                'user':'ZABBIX',
                'password':'P2633706298'
                },
                
        'KS7457':{
                'user':'ZABBIX',
                'password':'P2536437362'
                },
                
        'KS7459':{
                'user':'ZABBIX',
                'password':'P2566065293'
                },
                
        'KS7460':{
                'user':'ZABBIX',
                'password':'P2564684609'
                },
                
        'KS7464':{
                'user':'ZABBIX',
                'password':'P2535888694'
                },
                
        'KS7465':{
                'user':'ZABBIX',
                'password':'P2551898980'
                },
                
        'KS7466':{
                'user':'ZABBIX',
                'password':'P2539909254'
                },
                
        'KS7467':{
                'user':'ZABBIX',
                'password':'P2535829166'
                },
                
        'KS7468':{
                'user':'ZABBIX',
                'password':'P2553617741'
                },
                
        'KS7469':{
                'user':'ZABBIX',
                'password':'P2549823571'
                },
                
        'KS7470':{
                'user':'ZABBIX',
                'password':'P2536953664'
                },
                
        'KS7471':{
                'user':'ZABBIX',
                'password':'P2552298233'
                },
                
        'KS7475':{
                'user':'ZABBIX',
                'password':'P2559473166'
                },
                
        'KS7476':{
                'user':'ZABBIX',
                'password':'P2539027065'
                },
                
        'KS7477':{
                'user':'ZABBIX',
                'password':'P2536955534'
                },
                
        'KS7479':{
                'user':'ZABBIX',
                'password':'P2535884037'
                },
                
        'KS7480':{
                'user':'ZABBIX',
                'password':'P2537019814'
                },
                
        'KS7481':{
                'user':'ZABBIX',
                'password':'P2544476679'
                },
                
                
        'KS7483':{
                'user':'ZABBIX',
                'password':'P2545073686'
                },
                
        'KS7484':{
                'user':'ZABBIX',
                'password':'P2551826861'
                },
                
        'KS7486':{
                'user':'ZABBIX',
                'password':'P2543868869'
                },
                
        'KS7487':{
                'user':'ZABBIX',
                'password':'P2543618829'
                },
                
        'KS7488':{
                'user':'ZABBIX',
                'password':'P2542643997'
                },
                
        'KS7489':{
                'user':'ZABBIX',
                'password':'P2542560706'
                },
                
        'KS7500':{
                'user':'ZABBIX',
                'password':'P2538232695'
                },
                
        'KS7501':{
                'user':'ZABBIX',
                'password':'P2536601869'
                },
                
        'KS7502':{
                'user':'ZABBIX',
                'password':'P2539299966'
                },
                
        'KS7503':{
                'user':'ZABBIX',
                'password':'P2539382812'
                },
                
        'KS7505':{
                'user':'ZABBIX',
                'password':'P2568495701'
                },
                
        'KS7506':{
                'user':'ZABBIX',
                'password':'P2565434439'
                },
                
        'KS7507':{
                'user':'ZABBIX',
                'password':'P2567814079'
                },
                
        'KS7508':{
                'user':'ZABBIX',
                'password':'P2566464856'
                },
                
        'KS7509':{
                'user':'ZABBIX',
                'password':'P2570116821'
                },
                
        'KS7511':{
                'user':'ZABBIX',
                'password':'P2570126542'
                },
                
        'KS7515':{
                'user':'ZABBIX',
                'password':'P2537468532'
                },
                
        'KS7520':{
                'user':'ZABBIX',
                'password':'P2564174219'
                },
                
        'KS7531':{
                'user':'ZABBIX',
                'password':'P2511624465'
                },
                
        'KS7532':{
                'user':'ZABBIX',
                'password':'P2563748549'
                },
                
        'KS7533':{
                'user':'ZABBIX',
                'password':'P2549812349'
                },
                
        'KS7534':{
                'user':'ZABBIX',
                'password':'P2628974406'
                },
                
        'KS7541':{
                'user':'ZABBIX',
                'password':'P2563138905'
                },
                
        'KS7546':{
                'user':'ZABBIX',
                'password':'P2538841189'
                },
                
        'KS7548':{
                'user':'ZABBIX',
                'password':'P2569684380'
                },
                
        'KS7549':{
                'user':'ZABBIX',
                'password':'P2512486804'
                },
                
        'KS7550':{
                'user':'ZABBIX',
                'password':'P2515503927'
                },
                
        'KS7551':{
                'user':'ZABBIX',
                'password':'P2517391997'
                },
                
        'KS7552':{
                'user':'ZABBIX',
                'password':'P2519315232'
                },
                
        'KS7554':{
                'user':'ZABBIX',
                'password':'P2520514403'
                },
                
        'KS7556':{
                'user':'ZABBIX',
                'password':'P2600013052'
                },
                
        'KS7557':{
                'user':'ZABBIX',
                'password':'P2600014792'
                },
                
        'KS7565':{
                'user':'ZABBIX',
                'password':'P2632537563'
                },
                
        'KS7566':{
                'user':'ZABBIX',
                'password':'P2541251497'
                },
                
                
        'KS7569':{
                'user':'ZABBIX',
                'password':'P2539031674'
                },
                
        'KS7571':{
                'user':'ZABBIX',
                'password':'P2540675894'
                },
                
        'KS7572':{
                'user':'ZABBIX',
                'password':'P2606252436'
                },
                
        'KS7574':{
                'user':'ZABBIX',
                'password':'P2563804919'
                },
                
        'KS7575':{
                'user':'ZABBIX',
                'password':'P2535986198'
                },
                
        'KS7576':{
                'user':'ZABBIX',
                'password':'P2543964151'
                },
                
        'KS7578':{
                'user':'ZABBIX',
                'password':'P2544279837'
                },
                
        'KS7580':{
                'user':'ZABBIX',
                'password':'P2692377131'
                },
                
        'KS7583':{
                'user':'ZABBIX',
                'password':'P2733001351'
                },
                
        'KS7600':{
                'user':'ZABBIX',
                'password':'P2530295406'
                },
                
        'KS7606':{
                'user':'ZABBIX',
                'password':'P2559060673'
                },
                
        'KS7607':{
                'user':'ZABBIX',
                'password':'P2561579332'
                },
                
        'KS7608':{
                'user':'ZABBIX',
                'password':'P2619987415'
                },
                
        'KS7609':{
                'user':'ZABBIX',
                'password':'P2558365594'
                },
                
        'KS7612':{
                'user':'ZABBIX',
                'password':'P2549972922'
                },
                
                
                
                
                
        'KS8704':{
                'user':'ZABBIX',
                'password':'P2635614384'
                },
                
        'KS8705':{
                'user':'ZABBIX',
                'password':'P2635692038'
                },
                
        'KS8706':{
                'user':'ZABBIX',
                'password':'P2635692598'
                },
                
                
        'KS8708':{
                'user':'ZABBIX',
                'password':'P2635776303'
                },
                
        'KS8709':{
                'user':'ZABBIX',
                'password':'P2635778459'
                },
                
        'KS8710':{
                'user':'ZABBIX',
                'password':'P2635692878'
                },
                
        'KS8711':{
                'user':'ZABBIX',
                'password':'P2638710390'
                },
                
        'KS8712':{
                'user':'ZABBIX',
                'password':'P2768286375'
                },
                
        'KS8713':{
                'user':'ZABBIX',
                'password':'P2637425538'
                },
                
        'KS8714':{
                'user':'ZABBIX',
                'password':'P2637497450'
                },
                
        'KS8716':{
                'user':'ZABBIX',
                'password':'P2633706298'
                },
                
        'KS8718':{
                'user':'ZABBIX',
                'password':'P2633706298'
                },
                
        'KS8719':{
                'user':'ZABBIX',
                'password':'P2633706298'
                },
                
        'KS8720':{
                'user':'ZABBIX',
                'password':'P2633706298'
                },
                
        'KS8721':{
                'user':'ZABBIX',
                'password':'P2633706298'
                },
                
                
        'KS8724':{
                'user':'ZABBIX',
                'password':'P2633706298'
                },
                
        'KS8725':{
                'user':'ZABBIX',
                'password':'P2633706298'
                },
                
        'KS8726':{
                'user':'ZABBIX',
                'password':'P2633706298'
                },
                
        'KS8730':{
                'user':'ZABBIX',
                'password':'P2707163996'
                },
                
        'KS8732':{
                'user':'ZABBIX',
                'password':'P2734975315'
                },
                
        'KS8734':{
                'user':'ZABBIX',
                'password':'P2778258825'
                },
                
        'KS8735':{
                'user':'ZABBIX',
                'password':'P2756537864'
                },
                
        'KS8736':{
                'user':'ZABBIX',
                'password':'P2791488803'
                },
                
        'KS8738':{
                'user':'ZABBIX',
                'password':'P2806329243'
                },
                
        'KS8750':{
                'user':'ZABBIX',
                'password':'P2565557653'
                },
                
        'KS8751':{
                'user':'ZABBIX',
                'password':'P2549231907'
                },
                
        'KS8752':{
                'user':'ZABBIX',
                'password':'P2542548943'
                },
                
        'KS8753':{
                'user':'ZABBIX',
                'password':'P2553096997'
                },
                
        'KS8754':{
                'user':'ZABBIX',
                'password':'P2551889165'
                },
                
                
        'KS8756':{
                'user':'ZABBIX',
                'password':'P2549373199'
                },
                
        'KS8760':{
                'user':'ZABBIX',
                'password':'P2549409326'
                },
                
        'KS8761':{
                'user':'ZABBIX',
                'password':'P2597513303'
                },
                
        'KS8762':{
                'user':'ZABBIX',
                'password':'P2597531513'
                },
                
        'KS8763':{
                'user':'ZABBIX',
                'password':'P2597529728'
                },
                
        'KS8764':{
                'user':'ZABBIX',
                'password':'P2610385042'
                },
                
        'KS8765':{
                'user':'ZABBIX',
                'password':'P2610387197'
                },
                
        'KS8768':{
                'user':'ZABBIX',
                'password':'P2610390903'
                },
                
        'KS8769':{
                'user':'ZABBIX',
                'password':'P2565205915'
                },
                
        'KS8770':{
                'user':'ZABBIX',
                'password':'P2553703788'
                },
                
        'KS8771':{
                'user':'ZABBIX',
                'password':'P2542560473'
                },
                
        'KS8772':{
                'user':'ZABBIX',
                'password':'P2568557472'
                },
                
        'KS8773':{
                'user':'ZABBIX',
                'password':'P2568564822'
                },
                
        'KS8776':{
                'user':'ZABBIX',
                'password':'P2576529017'
                },
                
        'KS8778':{
                'user':'ZABBIX',
                'password':'P2576596632'
                },
                
        'KS8779':{
                'user':'ZABBIX',
                'password':'P2586351946'
                },
                
        'KS8787':{
                'user':'ZABBIX',
                'password':'P2514652244'
                },
                
        'KS9350':{
                'user':'ZABBIX',
                'password':'P2608567123'
                },
                
        'KS9356':{
                'user':'ZABBIX',
                'password':'P2608644676'
                },
                
        'KS9360':{
                'user':'ZABBIX',
                'password':'P2560453332'
                },
                
        'KS9361':{
                'user':'ZABBIX',
                'password':'P2564081185'
                },
                
        'KS9362':{
                'user':'ZABBIX',
                'password':'P2564756757'
                },
                
        'KS9370':{
                'user':'ZABBIX',
                'password':'P2633706298'
                },
                
        'KS9371':{
                'user':'ZABBIX',
                'password':'P2633706298'
                },
                
        'KS9373':{
                'user':'ZABBIX',
                'password':'P2633706298'
                },
                
        'KS9374':{
                'user':'ZABBIX',
                'password':'P2633706298'
                },
                
        'KS9375':{
                'user':'ZABBIX',
                'password':'P2633706298'
                },
                
        'KS9376':{
                'user':'ZABBIX',
                'password':'P2633706298'
                },
                
        'KS9377':{
                'user':'ZABBIX',
                'password':'P2633706298'
                },
                
        'KS9378':{
                'user':'ZABBIX',
                'password':'P2633706298'
                },
                
        'KS9379':{
                'user':'ZABBIX',
                'password':'P2633706298'
                },
                
        'KS9451':{
                'user':'ZABBIX',
                'password':'P2543862898'
                },
                
        'KS9459':{
                'user':'ZABBIX',
                'password':'P2567779822'
                },
                
        'KS9461':{
                'user':'ZABBIX',
                'password':'P2566419840'
                },
                
                
        'KS9466':{
                'user':'ZABBIX',
                'password':'P2529854108'
                },
                
        'KS9467':{
                'user':'ZABBIX',
                'password':'P2532295053'
                },
                
        'KS9469':{
                'user':'ZABBIX',
                'password':'P2559777953'
                },
                
        'KS9470':{
                'user':'ZABBIX',
                'password':'P2532792934'
                },
                
        'KS9471':{
                'user':'ZABBIX',
                'password':'P2533411349'
                },
                
        'KS9472':{
                'user':'ZABBIX',
                'password':'P2539016900'
                },
                
        'KS9473':{
                'user':'ZABBIX',
                'password':'P2539353097'
                },
                
        'KS9474':{
                'user':'ZABBIX',
                'password':'P2539364418'
                },
                
        'KS9476':{
                'user':'ZABBIX',
                'password':'P2550441023'
                },
                
        'KS9478':{
                'user':'ZABBIX',
                'password':'P2547399974'
                },
                
                
                
        'KS9481':{
                'user':'ZABBIX',
                'password':'P2539527663'
                },
                
        'KS9482':{
                'user':'ZABBIX',
                'password':'P2567282480'
                },
                
        'KS9488':{
                'user':'ZABBIX',
                'password':'P2550610754'
                },
                
        'KS9489':{
                'user':'ZABBIX',
                'password':'P2564850025'
                },
                
        'KS9490':{
                'user':'ZABBIX',
                'password':'P2566052303'
                },
                
        'KS9493':{
                'user':'ZABBIX',
                'password':'P2569718600'
                },
                
        'KS9500':{
                'user':'ZABBIX',
                'password':'P2633706298'
                },
                
        'KS9501':{
                'user':'ZABBIX',
                'password':'P2633706298'
                },
                
        'KS9502':{
                'user':'ZABBIX',
                'password':'P2633706298'
                },
                
        'KS9504':{
                'user':'ZABBIX',
                'password':'P2540309656'
                },
                
        'KS9505':{
                'user':'ZABBIX',
                'password':'P2535644854'
                },
                
        'KS9507':{
                'user':'ZABBIX',
                'password':'P2531592674'
                },
                
        'KS9510':{
                'user':'ZABBIX',
                'password':'P2536847757'
                },
                
        'KS9511':{
                'user':'ZABBIX',
                'password':'P2633706298'
                },
                
        'KS9512':{
                'user':'ZABBIX',
                'password':'P2633706298'
                },
                
        'KS9513':{
                'user':'ZABBIX',
                'password':'P2547734125'
                },
                
        'KS9514':{
                'user':'ZABBIX',
                'password':'P2549305748'
                },
                
        'KS9515':{
                'user':'ZABBIX',
                'password':'P2666033386'
                },
                
        'KS9516':{
                'user':'ZABBIX',
                'password':'P2563034062'
                },
                
        'KS9517':{
                'user':'ZABBIX',
                'password':'P2555293960'
                },
                
        'KS9519':{
                'user':'ZABBIX',
                'password':'P2538770381'
                },
                
        'KS9524':{
                'user':'ZABBIX',
                'password':'P2540244279'
                },
                
        'KS9527':{
                'user':'ZABBIX',
                'password':'P2536423640'
                },
                
        'KS9529':{
                'user':'ZABBIX',
                'password':'P2648566733'
                },
                
        'KS9535':{
                'user':'ZABBIX',
                'password':'P2530902766'
                },
                
        'KS9538':{
                'user':'ZABBIX',
                'password':'P2539648179'
                },
                
        'KS9539':{
                'user':'ZABBIX',
                'password':'P2539614753'
                },
                
        'KS9605':{
                'user':'ZABBIX',
                'password':'P2537209094'
                },
                
        'KS9606':{
                'user':'ZABBIX',
                'password':'P2578925856'
                },
                
        'KS9609':{
                'user':'ZABBIX',
                'password':'P2554989162'
                },
                
        'KS9611':{
                'user':'ZABBIX',
                'password':'P2566511799'
                },
                
        'KS9617':{
                'user':'ZABBIX',
                'password':'P2566477734'
                },
                
        'KS9618':{
                'user':'ZABBIX',
                'password':'P2527784375'
                },
                
        'KS9619':{
                'user':'ZABBIX',
                'password':'P2546632318'
                },
                
        'KS9623':{
                'user':'ZABBIX',
                'password':'P2550821251'
                },
                
        'KS9624':{
                'user':'ZABBIX',
                'password':'P2527882343'
                },
                
        'KS9625':{
                'user':'ZABBIX',
                'password':'P2534095829'
                },
                        
        'KS9626':{
                'user':'ZABBIX',
                'password':'P2581440107'
                },
                
        'KS9627':{
                'user':'ZABBIX',
                'password':'P2581445754'
                },
                
        'KS9630':{
                'user':'ZABBIX',
                'password':'P2570977490'
                },
                
        'KS9631':{
                'user':'ZABBIX',
                'password':'P2570997960'
                },
                                
        'KS9633':{
                'user':'ZABBIX',
                'password':'P2609094309'
                },
                
        'KS9643':{
                'user':'ZABBIX',
                'password':'P2670280995'
                },
                
        'KS9689':{
                'user':'ZABBIX',
                'password':'P2563996400'
                },
                
        'KS9691':{
                'user':'ZABBIX',
                'password':'P2538840502'
                },
                
        'KS9703':{
                'user':'ZABBIX',
                'password':'P2624304722'
                },
                
        'KS9706':{
                'user':'ZABBIX',
                'password':'P2527623767'
                },
                
                
        'KS9716':{
                'user':'ZABBIX',
                'password':'P2551187282'
                },
                
        'KS9717':{
                'user':'ZABBIX',
                'password':'P2542481985'
                },
                
                
        'KS9722':{
                'user':'ZABBIX',
                'password':'P2553797166'
                },
                
        'KS9723':{
                'user':'ZABBIX',
                'password':'P2542468200'
                },
                
                
                
        'KS9728':{
                'user':'ZABBIX',
                'password':'P2550343867'
                },
                
        'KS9732':{
                'user':'ZABBIX',
                'password':'P2544192605'
                },
                
        'KS9733':{
                'user':'ZABBIX',
                'password':'P2547405444'
                },
                
                
                
        'KS9737':{
                'user':'ZABBIX',
                'password':'P2545094631'
                },
                
        'KS9740':{
                'user':'ZABBIX',
                'password':'P2544742544'
                },
                
        'KS9744':{
                'user':'ZABBIX',
                'password':'P2546707769'
                },
                
        'KS9745':{
                'user':'ZABBIX',
                'password':'P2546896607'
                },
                
        'KS9746':{
                'user':'ZABBIX',
                'password':'P2638717487'
                },
                
        'KS9747':{
                'user':'ZABBIX',
                'password':'P2556975697'
                },
                
        'KS9750':{
                'user':'ZABBIX',
                'password':'P2537131407'
                },
                
        'KS9753':{
                'user':'ZABBIX',
                'password':'P2543596946'
                },
                
        'KS9754':{
                'user':'ZABBIX',
                'password':'P2545157265'
                },
                
        'KS9762':{
                'user':'ZABBIX',
                'password':'P2548592224'
                },
                
        'KS9766':{
                'user':'ZABBIX',
                'password':'P2565784201'
                },
                
        'KS9767':{
                'user':'ZABBIX',
                'password':'P2568912886'
                },
                
        'KS9769':{
                'user':'ZABBIX',
                'password':'P2564927540'
                },
                
        'KS9771':{
                'user':'ZABBIX',
                'password':'P2563732757'
                },
                
                
        'KS9773':{
                'user':'ZABBIX',
                'password':'P2567787551'
                },
                
        'KS9774':{
                'user':'ZABBIX',
                'password':'P2568309556'
                },
                
        'KS9775':{
                'user':'ZABBIX',
                'password':'P2554847738'
                },
                
        'KS9777':{
                'user':'ZABBIX',
                'password':'P2554677404'
                },
                
        'KS9781':{
                'user':'ZABBIX',
                'password':'P2551189855'
                },
                
        'KS9782':{
                'user':'ZABBIX',
                'password':'P2734974494'
                },
                
        'KS9783':{
                'user':'ZABBIX',
                'password':'P2554392724'
                },
                
        'KS9785':{
                'user':'ZABBIX',
                'password':'P2542057290'
                },
                
                
        'KS9788':{
                'user':'ZABBIX',
                'password':'P2565532795'
                },
                
        'KS9789':{
                'user':'ZABBIX',
                'password':'P2541431135'
                },
                
        'KS9790':{
                'user':'ZABBIX',
                'password':'P2553103566'
                },
                
                
        'KS9796':{
                'user':'ZABBIX',
                'password':'P2558025515'
                },
                
                
                
                
}

dbquery = {
    'version': 'select FVS_ADMD.FA_INFO.GetDBVersion from dual;',
    'timeonserver': "SELECT TO_CHAR(SYSDATE,'HH24:MI DD.MM.YYYY')FROM DUAL;", 
    'dbstatus': "SELECT INSTANCE_NAME || ' ' || HOST_NAME || ' ' ||DATABASE_STATUS FROM v$instance;",
    'sgapga': "select Round(sum(bytes) / 1024 / 1024 , 0) Mb  from (select bytes  from v$sgastat  union   select value bytes      from v$sesstat s, v$statname n   where n.STATISTIC# = s.STATISTIC#    and n.name = 'session pga memory');",
    'scheduleupdate': "select a.cftpstarttime || ' ' || a.cftpendtime || ' | ' || a.cupdatestarttime || ' ' || a.cupdateendtime  from v_rp_schedule a;",
    'stateoutlet': "select t.istate from rb_cashreg.rc_otherbranchinfo t;",
    'dbsize': "SELECT BYTES FROM dba_data_files WHERE tablespace_name NOT IN ('UNDO', 'SYSTEM', 'SYSAUX');",
    'total_memory_pga_areas_all_session': "select  Round (sum(value) / 1024 / 1024, 0) Mb   from v$sesstat s, v$statname n  where  n.STATISTIC# = s.STATISTIC#  and  name = 'session pga memory';",
    'fraused': "SELECT ROUND((SPACE_USED - SPACE_RECLAIMABLE)/SPACE_LIMIT * 100, 1)  FROM V$RECOVERY_FILE_DEST;",
    'repl_import_disabled': "select  state  from dba_scheduler_jobs where job_name = 'REPL_IMPORT' ;",
    'timelastoperation': "select TO_CHAR (MAX (a.ddate), 'HH24:MI DD.MM.YYYY') maxdate from rb_bis.v a where trunc(a.ddate) = trunc(sysdate);",
    'db_tablespace_users_perc_of_max': "select round(sum(bytes)/1024/1024 / 4000 * 100, 1)   from dba_data_files a  where a.tablespace_name = 'USERS'  group by a.tablespace_name; ",
    'backupstate':  "SELECT TO_CHAR (MAX (a.end_time), 'HH24:MI DD.MM.YYYY') maxdate FROM v$rman_status a WHERE operation = 'BACKUP' AND STATUS = 'COMPLETED' ORDER BY start_time DESC;",
    'session_ServiceInAS':  "select a.sid, a.module, a.logon_time from   v$session a  where  a.MODULE = 'SeviceInAs.exe';",
    'session_ServiceOutAS':  "select a.sid, a.module, a.logon_time from   v$session a  where  a.MODULE = 'ServiceOutAs.exe';",
    'bis_availability':  "select count(*) from v$session a  where  a.MODULE = 'SeviceInAs.exe' or a.MODULE = 'ServiceOutAs.exe';",
     }


def sender(key, value):
    zabbix = '10.45.129.32'
    popen("zabbix_sender -z {0} -s {1} -k {2} -o '{3}'".format(zabbix,DSN,key,value)) 


def complex(query, items):
    ## Use this for columns
    cursor.execute(query)
    row = cursor.fetchall()
    lst = [item[1] for item in row]
    lst = zip(items, lst)
    for item in lst:
        sender(str(item[0]), str(item[1]))

   

def jsonencode(jlist, title=''):
    data = '{{"data":{0} }}'.format(str(jlist).replace("'", ""))
    sender(title, data)


def toad(query, items):
    ## Use it for rows
    cursor.execute(query)
    row = cursor.fetchone()
    lst = zip(items,row)
    for item in lst:
        sender(item[0], int(item[1]))

environ['ORACLE_HOME'] = '/usr/lib/oracle/12.1/client64' 
connect = pyodbc.connect('DSN={0};UID={1};PWD={2};'.format(DSN, CRED[DSN]['user'], CRED[DSN]['password']))
cursor = connect.cursor()
for k in dbquery:
    try:
        cursor.execute(dbquery[k])
        row = cursor.fetchone()
        sender(k, row[0])
    except TypeError:
        sender(k, 'n/a')
print "OK"
