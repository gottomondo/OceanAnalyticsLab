# Ocean Analytics Lab
OceanAnalyticsLab is the place for the revise along the time of different solutions that scientific algorithms,
in the field of the Ocean Science, can adopt to improve the implementation of the Open Science approach.
The sketch of achievements presented here, concerns and can improve the evolution plan of community algorithms, 
when the exploitation limit is reached, but still much lower than its _theoretical_ upper bound. 

The implementation of those algorithms inside the community research infrastructures, will indeed deal with
[the interoperability and reusability challenge](#12---the-interoperability-and-reusability-challenge), 
that is a fundamental milestone to overcome before scaling up and targeting more ambitious projects.

The first contribution to this repository comes from the [VLab Marine Environmental Indicators](#11-the-vlab-marine-environmental-indicators), 
and shows the effectiveness of the implemented framework, based on the [MEI Development Toolkit](#1---mei-development-toolkit), 
for a prompt deploy of algorithms in a production environment, considering as initial and fundamental needs, 
those related to the input data access, and those related to the interoperability among algorithms and other network services.


## 1 - MEI Development Toolkit

This toolkit aims to underpin the development of scientific algorithms which are exploiting geospatial data 
for the extraction of new knowledge and indicators to serve the decision makers.
The considered scope is related to the environment protection and sustainable Blue Economy.

###### References
- **The Global Risks Report 2022**, 17th Edition, World Economic Forum, ISBN: 978-2-940631-09-4
- Alvarez Fanjul, E., Ciliberti, S. and Bahurel, P. (eds) (2022) **Implementing Operational Ocean Monitoring and Forecasting Systems**. Paris, France, IOC-UNESCO, 376pp. & Annexes, (GOOS-275). DOI: http://dx.doi.org/10.25607/OBP-1774
- Stefano Nativi, Mattia Santoro, Gregory Giuliani & Paolo Mazzetti (2020) **Towards a knowledge base to support global change policy goals**, International Journal of Digital Earth, 13:2, 188-216, DOI: 10.1080/17538947.2018.1559367
- Tintoré J, Pinardi N, Álvarez-Fanjul E, Aguiar E, Álvarez-Berastegui D, Bajo M, Balbin R, Bozzano R, Nardelli BB, Cardin V, Casas B, Charcos-Llorens M, Chiggiato J, Clementi E, Coppini G, Coppola L, Cossarini G, Deidun A, Deudero S, D'Ortenzio F, Drago A, Drudi M, El Serafy G, Escudier R, Farcy P, Federico I, Fernández JG, Ferrarin C, Fossi C, Frangoulis C, Galgani F, Gana S, García Lafuente J, Sotillo MG, Garreau P, Gertman I, Gómez-Pujol L, Grandi A, Hayes D, Hernández-Lasheras J, Herut B, Heslop E, Hilmi K, Juza M, Kallos G, Korres G, Lecci R, Lazzari P, Lorente P, Liubartseva S, Louanchi F, Malacic V, Mannarini G, March D, Marullo S, Mauri E, Meszaros L, Mourre B, Mortier L, Muñoz-Mas C, Novellino A, Obaton D, Orfila A, Pascual A, Pensieri S, Pérez Gómez B, Pérez Rubio S, Perivoliotis L, Petihakis G, de la Villéon LP, Pistoia J, Poulain P-M, Pouliquen S, Prieto L, Raimbault P, Reglero P, Reyes E, Rotllan P, Ruiz S, Ruiz J, Ruiz I, Ruiz-Orejón LF, Salihoglu B, Salon S, Sammartino S, Sánchez Arcilla A, Sánchez-Román A, Sannino G, Santoleri R, Sardá R, Schroeder K, Simoncelli S, Sofianos S, Sylaios G, Tanhua T, Teruzzi A, Testor P, Tezcan D, Torner M, Trotta F, Umgiesser G, von Schuckmann K, Verri G, Vilibic I, Yucel M, Zavatarelli M and Zodiatis G (2019). **Challenges for Sustained Observing and Forecasting Systems in the Mediterranean Sea**. Front. Mar. Sci. 6:568. doi: 10.3389/fmars.2019.00568
- Mathieu, Pierre-Philippe and Aubrecht, Christoph. **Earth Observation Open Science and Innovation**. 2018. DOI: 10.1007/978-3-319-65633-5
- **United Nations Decade of Ocean Science for Sustainable Developments**, Challenges, https://www.oceandecade.org/challenges/

### 1.1 The VLab Marine Environmental Indicators
A new VLab for the environment monitoring was implemented inside the VRE framework D4Science, in the scope of Blue-Cloud EU project ([Grant Agreement No.862409](https://cordis.europa.eu/project/id/862409)).
The VLab aims to provide analytics services to those users who are involved in the monitoring and management of marine areas.
The VLab, through the VRE framework, offers also several federated services to the scientific developers, for instance related to the data access, 
storage and processing, which ease the development of new innovative solutions, and also the sharing of results.

###### References
- **The VLab Marine Environmental Indicators**, https://blue-cloud.d4science.org/web/marineenvironmentalindicators/
- Drago, Federico; Cabrera, Patricia; Irisson, Jean-Olivier; Bittner, Lucie; Schickele, Alexandre; Drudi, Massimiliano; Balem, Kevin; Noteboom, Jan Willem; Castaño-Primo, Rocío; Jones, Steve; Taconet, Marc; Ellenbroek, Anton; Vallejo, Bryan R.; Haberle, Ines; Hackenberger, Domagoj K; Djerdj, Tamara; Hackenberger, Branimir K.; Ćaleta, Bruno; Purgar, Marija; Kapetanović, Damir; Marn, Nina; Pečar Ilić, Jadranka; Klanjšček, Tin; Gómez Navarro, Laura; Jongedijk, Cleo; Kaandorp, Mikael; Lobelle, Delphine; Manral, Darshika; Onink, Victor; Pierard, Claudio; Richardson, Joey; Zavala-Romero, Olmo. (2023). **Blue-Cloud Virtual Labs in support of Sustainable Development Goals**. Zenodo. https://doi.org/10.5281/zenodo.7663960
- Julia Vera, Sara Pittonet, Dick Schaap, Pasquale Pagano, Patricia Cabrera, Jean-Olivier Irisson, Massimiliano Drudi, Anton Ellenbroek, Andreas Petzold, Marina Tonani, Akrivi Vivian Kiousi, Tiziana Ferrari, Laurent Delauney, & Marc Taconet. (2022, December 8). B**lue-Cloud final conference slides**. Zenodo. https://doi.org/10.5281/zenodo.7438715
- Vera, Julia, Larkin, Kate, Delaney, Conor, Tonné, Nathalie, Cisternino, Stefano, Calewaert, Jan-Bart, Pittonet Gaiarin, Sara, Drago, Federico, Schaap, Dick, Pagano, Pasquale, Cabrera, Patricia, Drudi, Massimiliano, Ellenbroek, Anton, & Obaton, Dominique. (2022, November 29). **Blue-Cloud Strategic Roadmap - Executive summary (supporting material for Final Conference)**. https://doi.org/10.5281/zenodo.7377985
- Drudi, Massimiliano; Balem, Kevin; Noteboom, Jan Willem; Castaño-Primo, Rocío; Jones, Steve; Blue-Cloud Project, Fact Sheet. (2022, Nov 4). **Marine Environmental Indicators**. https://doi.org/10.5281/zenodo.7292455
- Drudi, Massimiliano; Palermo, Francesco; Mariani, Antonio; Lecci, Rita; Garcia Juan, Andrea; Balem, Kevin; Maze, Guillaume; Bachelot, Loïc; Noteboom, Jan Willem; Pfeil, Benjamin; Castaño-Primo, Rocío; Paul, Julien; Dussurget, Renaud; Arnaud, Alain. (2022). Blue-Cloud Project, presentation. (2022, May 25). **Test the Blue-Cloud Virtual Labs: Marine Environmental Indicators**. https://doi.org/10.5281/zenodo.6628701 
- Balem Kevin, Garcia Juan Andrea, Bachelot Loïc, & Maze Guillaume. (2022, May 25). Blue-Cloud project, presentation. **Blue-Cloud Marine Environmental Indicators Virtual Lab - The Ocean Regimes Notebook**. Zenodo. https://doi.org/10.5281/zenodo.6584430
- Pittonet Sara, Giuffrida Rita, Mari Marialetizia, & Schaap Dick. (2022). Blue-Cloud Project, Deliverable D6.1, **Fact Sheets for cluster projects and other core initiatives** (Release 1) (Version 1). Zenodo. https://doi.org/10.5281/zenodo.5549789
- Bachelot Loïc, Balem Kevin, Drago Federico, Drudi Massimiliano, & Garcia Juan Andrea. (2021). Blue-Cloud project, report. **Applying machine learning methods to ocean patterns and ocean regimes indicators**. Zenodo. https://doi.org/10.5281/zenodo.5896651
- Pearlman J, Buttigieg PL, Bushnell M, Delgado C, Hermes J, Heslop E, Hörstmann C, Isensee K, Karstensen J, Lambert A, Lara-Lopez A, Muller-Karger F, Munoz Mas C, Pearlman F, Pissierssens P, Przeslawski R, Simpson P, van Stavel J and Venkatesan R (2021) **Evolving and Sustaining Ocean Best Practices to Enable Interoperability in the UN Decade of Ocean Science for Sustainable Development**. Front. Mar. Sci. 8:619685. doi: 10.3389/fmars.2021.619685
- M. Assante, L. Candela, D. Castelli, R. Cirillo, G. Coro, L. Frosini, L. Lelii, F. Mangiacrapa, P. Pagano, G. Panichi, F. Sinibaldi, **Enacting open science by D4Science, Future Generation Computer Systems**, Volume 101, 2019, Pages 555-563, ISSN 0167-739X, https://doi.org/10.1016/j.future.2019.05.063.
- Santoro, M.; Mazzetti, P.; Nativi, S. **The VLab Framework: An Orchestrator Component to Support Data to Knowledge Transition**. Remote Sens. 2020, 12, 1795. https://doi.org/10.3390/rs12111795
- Pearlman J, Bushnell M, Coppola L, Karstensen J, Buttigieg PL, Pearlman F, Simpson P, Barbier M, Muller-Karger FE, Munoz-Mas C, Pissierssens P, Chandler C, Hermes J, Heslop E, Jenkyns R, Achterberg EP, Bensi M, Bittig HC, Blandin J, Bosch J, Bourles B, Bozzano R, Buck JJH, Burger EF, Cano D, Cardin V, Llorens MC, Cianca A, Chen H, Cusack C, Delory E, Garello R, Giovanetti G, Harscoat V, Hartman S, Heitsenrether R, Jirka S, Lara-Lopez A, Lantéri N, Leadbetter A, Manzella G, Maso J, McCurdy A, Moussat E, Ntoumas M, Pensieri S, Petihakis G, Pinardi N, Pouliquen S, Przeslawski R, Roden NP, Silke J, Tamburri MN, Tang H, Tanhua T, Telszewski M, Testor P, Thomas J, Waldmann C and Whoriskey F (2019) **Evolving and Sustaining Ocean Best Practices and Standards for the Next Decade**. Front. Mar. Sci. 6:277. doi: 10.3389/fmars.2019.00277
- Buck JJH, Bainbridge SJ, Burger EF, Kraberg AC, Casari M, Casey KS, Darroch L, Rio JD, Metfies K, Delory E, Fischer PF, Gardner T, Heffernan R, Jirka S, Kokkinaki A, Loebl M, Buttigieg PL, Pearlman JS and Schewe I (2019) **Ocean Data Product Integration Through Innovation-The Next Level of Data Interoperability**. Front. Mar. Sci. 6:32. doi: 10.3389/fmars.2019.00032
- Coppini, G., Marra, P., Lecci, R., Pinardi, N., Cretì, S., Scalas, M., Tedesco, L., D'Anca, A., Fazioli, L., Olita, A., Turrisi, G., Palazzo, C., Aloisio, G., Fiore, S., Bonaduce, A., Kumkar, Y. V., Ciliberti, S. A., Federico, I., Mannarini, G., Agostini, P., Bonarelli, R., Martinelli, S., Verri, G., Lusito, L., Rollo, D., Cavallo, A., Tumolo, A., Monacizzo, T., Spagnulo, M., Sorgente, R., Cucco, A., Quattrocchi, G., Tonani, M., Drudi, M., Nassisi, P., Conte, L., Panzera, L., Navarra, A., and Negro, G.: **SeaConditions: a web and mobile service for safer professional and recreational activities in the Mediterranean Sea**, Nat. Hazards Earth Syst. Sci., 17, 533–547, https://doi.org/10.5194/nhess-17-533-2017, 2017
- United Nations Decade of Ocean Science for Sustainable Developments, Challenges, "**Challenge 9 - Skills, knowledge and technology for all**", https://www.oceandecade.org/challenges/

### 1.2 - The Interoperability and Reusability Challenge
The exploitation of datasets and algorithms, without barriers for the scientific investigation, is a highly desired condition, 
and for the pursuing of this objective, the interoperability aspects play an important role, because it opens the door 
to the reuse of verified/validated functionalities in multiple systems or projects, which is a fundamental condition for implementing the Open Science. 
Indeed, the toolkit copes several specific issues, that can raise when working with federated services, such as in the case of 
VLab _Marine Environmental Indicators_.

The toolkit aims to ease the transition of mature algorithms to production environment 
and to maximize the exploitation of resources which are already available on research and data infrastructures. 
Furthermore, one expected outcome from using this toolkit, is the capability to compose, or extend with a reasonable effort, 
new customized analytics services, embracing according to the needs, a different selection of data sources and processing services.

The toolkit includes and implements the following functionalities:
- procedure and template for implementing a scientific algorithm as processing service (OGC WPS)
- data access functionalities, based on a generalized API definition
- reader of input parameters, based on a generalized IDL
- manager of logging/provenance information (will be based on W3C-PROV)
- preview plot generator, applicable to NetCDF data format, convention CF-xx

###### References
- Hoogenkamp Bram, Farshidi Siamak, Xin Ruyue, Shi Zeshun, Chen Peng, & Zhao Zhiming. (2022, March 22). conference paper. **A Decentralized Service Control framework for Decentralized Applications in Cloud Environments**. 9th European Conference On Service-Oriented And Cloud Computing (ESOCC), Online. https://doi.org/10.1007/978-3-031-04718-3_4
- Wang, Yuandou; Zhao, Zhiming. (2020, October 18). **Decentralized workflow management on software defined infrastructure**. Workshop on The 1st Workshop On Data-Centric Workflows On Heterogeneous Infrastructures: Challenges And Directions (DAWHI), in the context of IEEE Service Congress (DAWHI, IEEE Service), Online. https://doi.org/10.1109/SERVICES48979.2020.00059
- Carlos Osuna, Joerg Behrens, Reinhard Budich, Willem Deconinck, Julia Duras, Italo Epicoco, Oliver Fuhrer, Christian Kühnlein, Leonidas Linardakis, Tobias Wicky, Nils Wedi. D2.1: **High-level Domain Specific Language (DSL) specification**. Version 1.0, 23 March 2019. Public report published by project ESCAPE-2, EU Grant Agreement No. 958927  
- National Academies of Sciences, Engineering, and Medicine. 2019. **Reproducibility and Replicability in Science**. Washington, DC: The National Academies Press. https://doi.org/10.17226/25303.
- Tanhua T, Pouliquen S, Hausman J, O’Brien K, Bricher P, de Bruin T, Buck JJH, Burger EF, Carval T, Casey KS, Diggs S, Giorgetti A, Glaves H, Harscoat V, Kinkade D, Muelbert JH, Novellino A, Pfeil B, Pulsifer PL, Van de Putte A, Robinson E, Schaap D, Smirnov A, Smith N, Snowden D, Spears T, Stall S, Tacoma M, Thijsse P, Tronstad S, Vandenberghe T, Wengren M, Wyborn L and Zhao Z (2019) **Ocean FAIR Data Services**. Front. Mar. Sci. 6:440. doi: 10.3389/fmars.2019.00440
- European Commission, Directorate-General for Research and Innovation, **Turning FAIR into reality** : final report and action plan from the European Commission expert group on FAIR data, Publications Office, 2018, https://data.europa.eu/doi/10.2777/1524
- D'Anca, A., Conte, L., Nassisi, P., Palazzo, C., Lecci, R., Cretì, S., Mancini, M., Nuzzo, A., Mirto, M., Mannarini, G., Coppini, G., Fiore, S., and Aloisio, G.: **A multi-service data management platform for scientific oceanographic products**, Nat. Hazards Earth Syst. Sci., 17, 171–184, https://doi.org/10.5194/nhess-17-171-2017, 2017
- Héder, Mihály. (2017). **From NASA to EU: the evolution of the TRL scale in Public Sector Innovation**. Innovation Journal. Volume 22, Issue 2, 2017. URL: https://www.innovation.cc/volumes-issues/vol22-no2.htm
- Paul Groth; Luc Moreau; eds. **PROV-OVERVIEW: An Overview of the PROV Family of Document**s. 30 April 2013, W3C Note. URL: http://www.w3.org/TR/2013/NOTE-prov-overview-20130430/
- Stodden, Victoria, **The Scientific Method in Practice: Reproducibility in the Computational Sciences** (February 9, 2010). MIT Sloan Research Paper No. 4773-10, Available at SSRN: https://ssrn.com/abstract=1550193 or http://dx.doi.org/10.2139/ssrn.1550193
- Joseph P. Cavano and James A. McCall. 1978. **A framework for the measurement of software quality**. In Proceedings of the software quality assurance workshop on Functional and performance issues. Association for Computing Machinery, New York, NY, USA, 133–139. https://doi.org/10.1145/800283.811113
- Open Geospatial Consortium, **Web Processing Service** (OGC WPS), https://www.ogc.org/standards/wps
- **PANGEO**, A community platform for Big Data geoscience, https://pangeo.io/

