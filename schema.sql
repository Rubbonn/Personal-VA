-- --------------------------------------------------------

--
-- Struttura della tabella `aeromobili`
--

CREATE TABLE `aeromobili` (
  `id` smallint(5) NOT NULL PRIMARY KEY,
  `nome` varchar(64) NOT NULL,
  `capacita_serbatoio_l` smallint(6) NOT NULL,
  `consumo_l_h` decimal(8,6) NOT NULL,
  `numero_posti` smallint(6) NOT NULL,
  `velocita_massima_kn` smallint(6) NOT NULL,
  `velocita_crocera_kn` smallint(6) NOT NULL,
  `grandezza_stiva_kg` decimal(5,2) NOT NULL,
  `foto` varchar(64) NOT NULL
);

--
-- Dump dei dati per la tabella `aeromobili`
--

INSERT INTO `aeromobili` (`id`, `nome`, `capacita_serbatoio_l`, `consumo_l_h`, `numero_posti`, `velocita_massima_kn`, `velocita_crocera_kn`, `grandezza_stiva_kg`, `foto`) VALUES
(1, 'Cessna C172', 212, '35.961395', 2, 145, 100, '54.43', 'cessna-c172.webp');

-- --------------------------------------------------------

--
-- Struttura della tabella `aeroporti`
--

CREATE TABLE `aeroporti` (
  `id` smallint(5) NOT NULL PRIMARY KEY,
  `codice_icao` char(4) NOT NULL,
  `nome` varchar(64) NOT NULL,
  `citta` varchar(64) NOT NULL,
  `nazione` char(3) NOT NULL,
  `latitudine` decimal(17,15) NOT NULL,
  `longitudine` decimal(18,15) NOT NULL
);

--
-- Dump dei dati per la tabella `aeroporti`
--

INSERT INTO `aeroporti` (`id`, `codice_icao`, `nome`, `citta`, `nazione`, `latitudine`, `longitudine`) VALUES
(1, 'LIVV', 'Vische', 'Vische', 'ITA', '45.347222222222220', '7.921388888888889'),
(2, 'LIRZ', 'San Francesco', 'Perugia', 'ITA', '43.097222222222220', '12.510277777777778'),
(3, 'LIRV', 'Viterbo', 'Viterbo', 'ITA', '42.430277777777775', '12.064166666666667'),
(4, 'LIRU', 'Urbe', 'Rome', 'ITA', '41.951944444444450', '12.500833333333333'),
(5, 'LIRN', 'Capodichino', 'Naples', 'ITA', '40.884444444444440', '14.290833333333333'),
(6, 'LIRM', 'Grazzanise', 'Grazzanise', 'ITA', '41.061997222222220', '14.082688888888889'),
(7, 'LIRJ', 'Marina Di Campo', 'Marina Di Campo', 'ITA', '42.761111111111110', '10.239722222222222'),
(8, 'LIRI', 'Pontecagnano', 'Salerno', 'ITA', '40.620000000000000', '14.912500000000000'),
(9, 'LIRH', 'Frosinone', 'Frosinone', 'ITA', '41.644925000000000', '13.299022222222222'),
(10, 'LIRG', 'Guidonia', 'Guidonia', 'ITA', '41.996111111111110', '12.734722222222220'),
(11, 'LIRF', 'Fiumicino', 'Rome', 'ITA', '41.800277777777770', '12.238888888888889'),
(12, 'LIRE', 'Pratica Di Mare', 'Pratica Di Mare', 'ITA', '41.659372222222224', '12.445155555555555'),
(13, 'LIRA', 'Ciampino', 'Rome', 'ITA', '41.799444444444440', '12.597222222222223'),
(14, 'LIKO', 'Guglielmo Zamboni', 'Ozzano Emilia', 'ITA', '44.475000000000000', '11.541666666666666'),
(15, 'LIPX', 'Villafranca', 'Verona', 'ITA', '45.396388888888886', '10.887777777777778'),
(16, 'LIMG', 'Albenga', 'Albenga', 'ITA', '44.045833333333334', '8.125555555555556'),
(17, 'LIEA', 'Fertilia', 'Alghero', 'ITA', '40.631111111111110', '8.288611111111111'),
(18, 'LIPR', 'Rimini', 'Rimini', 'ITA', '44.019444444444446', '12.609444444444444'),
(19, 'LILO', 'Caiolo', 'Sondrio', 'ITA', '46.150000000000000', '9.800000000000000'),
(20, 'LIPQ', 'Ronchi Dei Legionari', 'Trieste', 'ITA', '45.827500000000000', '13.472222222222223'),
(21, 'LI23', 'Bore Di Chienti', 'Corridonia', 'ITA', '43.261000000000000', '13.564666666666668'),
(22, 'LIPN', 'Boscomantico', 'Verona', 'ITA', '45.473055555555554', '10.926944444444445'),
(23, 'LIPL', 'Ghedi', 'Ghedi', 'ITA', '45.435736111111105', '10.270280555555557'),
(24, 'LIPI', 'Rivolto', 'Rivolto', 'ITA', '45.980691666666665', '13.049900000000000'),
(25, 'LIPG', 'Gorizia', 'Gorizia', 'ITA', '45.906666666666666', '13.599166666666667'),
(26, 'LIPF', 'Ferrara', 'Ferrara', 'ITA', '44.815833333333330', '11.613333333333333'),
(27, 'LINL', 'Lepore', 'Lecce', 'ITA', '40.357500000000000', '18.293888888888890'),
(28, 'LIMZ', 'Levaldigi', 'Cuneo', 'ITA', '44.547500000000000', '7.623055555555556'),
(29, 'LINB', 'Corte', 'Melpignano', 'ITA', '40.106388888888890', '18.257500000000000'),
(30, 'LIMW', 'Aosta', 'Aosta', 'ITA', '45.738333333333340', '7.367500000000000'),
(31, 'LI34', 'Mensanello', 'Mensanello', 'ITA', '43.369722222222220', '11.125000000000000'),
(32, 'LIKE', 'Alicaorle', 'Caorle', 'ITA', '45.611944444444450', '12.814611111111113'),
(33, 'LIMF', 'Caselle', 'Torino', 'ITA', '45.202500000000000', '7.649444444444444'),
(34, 'LIMA', 'Aeritalia', 'Torino', 'ITA', '45.084444444444440', '7.603055555555555'),
(35, 'LIMR', 'Novi Ligure', 'Novi Ligure', 'ITA', '44.780000000000000', '8.786388888888888'),
(36, 'LIMP', 'Parma', 'Parma', 'ITA', '44.822222222222220', '10.295277777777777'),
(37, 'LIPS', 'Istrana', 'Treviso', 'ITA', '45.684866666666665', '12.082880555555555'),
(38, 'LILV', 'Valbrembo', 'Valbrembo', 'ITA', '45.720555555555556', '9.593611111111112'),
(39, 'LIML', 'Linate', 'Milan', 'ITA', '45.449444444444440', '9.278333333333334'),
(40, 'LIAF', 'Foligno', 'Foligno', 'ITA', '42.932777777777770', '12.709999999999999'),
(41, 'LIMJ', 'Sestri', 'Genoa', 'ITA', '44.413333333333334', '8.837500000000000'),
(42, 'LIMN', 'Cameri', 'Cameri', 'ITA', '45.531108333333336', '8.665236111111112'),
(43, 'LIBR', 'Casale', 'Brindisi', 'ITA', '40.660555555555554', '17.948055555555555'),
(44, 'LICC', 'Fontanarossa', 'Catania', 'ITA', '37.466666666666670', '15.063888888888890'),
(45, 'LI28', 'Vigarolo', 'Vigarolo', 'ITA', '45.218333333333334', '9.468333333333334'),
(46, 'LILY', 'Como', 'Como', 'ITA', '45.814722222222220', '9.069722222222222'),
(47, 'LILR', 'Migliaro', 'Cremona', 'ITA', '45.167222222222220', '10.001944444444444'),
(48, 'LILN', 'Venegono', 'Varese', 'ITA', '45.741388888888890', '8.886666666666667'),
(49, 'LICT', 'Birgi', 'Trapani', 'ITA', '37.912058333333334', '12.493438888888887'),
(50, 'LILF', 'Castelnuovo Don Bosco', 'Castelnuovo Don Bosco', 'ITA', '45.024444444444440', '7.966388888888889'),
(51, 'LIPB', 'Bolzano', 'Bolzano', 'ITA', '46.460277777777780', '11.326388888888890'),
(52, 'LILG', 'Vergiate', 'Vergiate', 'ITA', '45.714444444444446', '8.699722222222222'),
(53, 'LI22', 'Il Gabbiano', 'San Vincenzo', 'ITA', '43.051666666666660', '10.552500000000000'),
(54, 'LI38', 'Parco Livenza', 'San Stino di Livenza', 'ITA', '45.736666666666665', '12.705555555555556'),
(55, 'LILE', 'Cerrione', 'Biella', 'ITA', '45.495833333333340', '8.102500000000000'),
(56, 'LILC', 'Calcinate del Pesce', 'Calcinate del Pesce', 'ITA', '45.809722222222220', '8.768055555555556'),
(57, 'LIQF', 'Palazzolo', 'Sansepolcro', 'ITA', '43.561944444444440', '12.154444444444445'),
(58, 'LICG', 'Pantelleria', 'Pantelleria', 'ITA', '36.813055555555550', '11.960833333333333'),
(59, 'LI30', 'Piacenza', 'Gragnano', 'ITA', '45.000000000000000', '9.583333333333334'),
(60, 'LILB', 'Alzate Brianza', 'Alzate Brianza', 'ITA', '45.769999999999996', '9.160833333333334'),
(61, 'LIPU', 'Padova', 'Padova', 'ITA', '45.396111111111110', '11.848055555555556'),
(62, 'LIDH', 'Thiene', 'Thiene', 'ITA', '45.675555555555555', '11.496388888888887'),
(63, 'LI21', 'Sagrantino', 'Gualdo Cattaneo', 'ITA', '42.890333333333330', '12.533027777777779'),
(64, 'LIAL', 'Sant''Illuminato', 'Citta di Castello', 'ITA', '43.355277777777780', '12.218333333333334'),
(65, 'LILA', 'Alessandria', 'Alessandria', 'ITA', '44.925000000000000', '8.625277777777779'),
(66, 'LI12', 'Montalto Dora', 'Ivrea', 'ITA', '45.489166666666670', '7.841666666666667'),
(67, 'LIMS', 'Piacenza', 'Piacenza', 'ITA', '44.913863888888890', '9.720586111111110'),
(68, 'LIQN', 'Rieti', 'Rieti', 'ITA', '42.426666666666660', '12.850000000000000'),
(69, 'LICR', 'Reggio Calabria', 'Reggio Calabria', 'ITA', '38.071944444444450', '15.653611111111111'),
(70, 'LIRP', 'San Giusto', 'Pisa', 'ITA', '43.682777777777770', '10.395555555555555'),
(71, 'LIAU', 'Capua', 'Capua', 'ITA', '41.115833333333335', '14.178055555555554'),
(72, 'LIKL', 'Comina', 'Pordenone', 'ITA', '45.991666666666670', '12.654444444444445'),
(73, 'LI04', 'Celano', 'Celano', 'ITA', '42.066666666666670', '13.533333333333333'),
(74, 'LIMC', 'Malpensa', 'Milan', 'ITA', '45.630000000000000', '8.723055555555556'),
(75, 'LIEE', 'Elmas', 'Cagliari', 'ITA', '39.247222222222220', '9.056111111111111'),
(76, 'LIDV', 'Prati Vecchi Di Aguscello', 'Prati Vecchi Di Aguscello', 'ITA', '44.790277777777774', '11.669166666666666'),
(77, 'LI24', 'Valle Gaffaro', 'Valle Gaffaro', 'ITA', '44.833333333333336', '12.232222222222223'),
(78, 'LILM', 'Casale Monferrato', 'Casale Monferrato', 'ITA', '45.111111111111114', '8.456111111111110'),
(79, 'LIDU', 'Budrione', 'Carpi', 'ITA', '44.835000000000000', '10.871666666666668'),
(80, 'LIDP', 'Pavullo', 'Pavullo', 'ITA', '44.322222222222220', '10.831666666666667'),
(81, 'LIDA', 'Asiago', 'Asiago', 'ITA', '45.887777777777780', '11.516666666666667'),
(82, 'LIDW', 'Carrer', 'Salgareda', 'ITA', '45.700000000000000', '12.543055555555556'),
(83, 'LIAP', 'Parchi', 'L''Aquila', 'ITA', '42.379444444444445', '13.309444444444445'),
(84, 'LI40', 'Vallesanta', 'Rieti', 'ITA', '42.427777777777780', '12.806388888888890'),
(85, 'LIDG', 'Lugo Di Romagna', 'Lugo Di Romagna', 'ITA', '44.398055555555560', '11.854722222222222'),
(86, 'LI14', 'Molinella', 'Molinella', 'ITA', '44.592777777777780', '11.655555555555557'),
(87, 'LI26', 'Piancada', 'Piancada', 'ITA', '45.764444444444440', '13.072222222222223'),
(88, 'LIDE', 'Reggio Emilia', 'Reggio Emilia', 'ITA', '44.698888888888890', '10.662500000000000'),
(89, 'LIPV', 'Lido', 'Venice', 'ITA', '45.428888888888885', '12.387777777777778'),
(90, 'LIMB', 'Bresso', 'Milan', 'ITA', '45.541388888888890', '9.202222222222222'),
(91, '', 'Dovera', 'Dovera', 'ITA', '45.380555555555550', '9.536666666666667'),
(92, 'LICZ', 'Sigonella', 'Catania', 'ITA', '37.405888888888890', '14.923908333333333'),
(93, 'LIPE', 'Borgo Panigale', 'Bologna', 'ITA', '44.530833333333334', '11.296944444444444'),
(94, 'LICP', 'Boccadifalco', 'Palermo', 'ITA', '38.110833333333330', '13.313333333333334'),
(95, 'LIBP', 'Pescara', 'Pescara', 'ITA', '42.437222222222220', '14.187222222222223'),
(96, 'LIDT', 'Mattarello', 'Trento', 'ITA', '46.023333333333330', '11.125000000000000'),
(97, 'LICB', 'Comiso', 'Comiso', 'ITA', '36.995833333333340', '14.608888888888888'),
(98, 'LICA', 'Lamezia Terme', 'Lamezia Terme', 'ITA', '38.908333333333330', '16.241666666666667'),
(99, 'LIPO', 'Montichiari', 'Brescia', 'ITA', '45.428888888888885', '10.330555555555556'),
(100, 'LI50', 'L''Aquila', 'L''Aquila', 'ITA', '42.300833333333330', '13.516666666666667'),
(101, 'LIQW', 'Luni', 'Sarzana', 'ITA', '44.088888888888890', '9.988888888888889'),
(102, 'LIBC', 'Crotone', 'Crotone', 'ITA', '38.996666666666670', '17.079166666666666'),
(103, 'LIBD', 'Palese', 'Bari', 'ITA', '41.138055555555550', '16.765000000000000'),
(104, 'LI25', 'Monte Marenzo', 'Lecco', 'ITA', '45.762000000000000', '9.445000000000000'),
(105, 'LIBN', 'Galatina', 'Lecce', 'ITA', '40.239227777777780', '18.133325000000000'),
(106, 'LIBA', 'Amendola', 'Amendola', 'ITA', '41.541391666666660', '15.718083333333334'),
(107, 'LIBV', 'Gioia Del Colle', 'Gioia Del Colle', 'ITA', '40.769700000000000', '16.933016666666667'),
(108, 'LI27', 'La Speziana', 'Spessa', 'ITA', '45.128611111111110', '9.363055555555555'),
(109, 'LIME', 'Orio Al Serio', 'Bergamo', 'ITA', '45.668888888888890', '9.700277777777776'),
(110, 'LILQ', 'Cinquale', 'Massa', 'ITA', '43.985833333333330', '10.142777777777777'),
(111, 'LIBF', 'Gino Lisa', 'Foggia', 'ITA', '41.433333333333330', '15.534722222222221'),
(112, 'LIAT', 'Valdera', 'Valdera', 'ITA', '43.591944444444444', '10.695555555555556'),
(113, 'LIBG', 'Grottaglie', 'Taranto', 'ITA', '40.517222222222220', '17.399722222222223'),
(114, 'LIPZ', 'Tessera', 'Venice', 'ITA', '45.505277777777780', '12.351944444444444'),
(115, 'LI11', 'San Giustino Valdarno', 'Il Borro', 'ITA', '43.540833333333330', '11.702499999999999'),
(116, 'LI06', 'Monteverdi M.', 'Consalvo', 'ITA', '43.116666666666670', '10.733333333333333'),
(117, 'LI31', 'Sabaudia', 'Sabaudia', 'ITA', '41.333611111111110', '13.021388888888890'),
(118, 'LI49', 'Boglietto', 'Boglietto', 'ITA', '44.758638888888890', '8.183250000000000'),
(119, 'LIAQ', 'Aquino', 'Aquino', 'ITA', '41.486111111111114', '13.718611111111110'),
(120, 'LIRS', 'Grosseto', 'Grosseto', 'ITA', '42.759722222222220', '11.071944444444444'),
(121, 'LIDL', 'Legnago', 'Legnago', 'ITA', '45.133055555555560', '11.292222222222222'),
(122, 'LIQQ', 'Castiglion Fiorentino', 'Serristori', 'ITA', '43.332500000000000', '11.858055555555556'),
(123, 'LI35', 'S. Apollonia', 'Montecchio-Podere', 'ITA', '43.295277777777780', '11.903333333333334'),
(124, 'LIRL', 'Latina', 'Latina', 'ITA', '41.546944444444440', '12.908333333333333'),
(125, 'LIPD', 'Campoformido', 'Udine', 'ITA', '46.031944444444440', '13.186666666666667'),
(126, 'LI37', 'Sant Apollinare', 'Sant Apollinare', 'ITA', '45.034250000000000', '11.822944444444444'),
(127, 'LIPY', 'Falconara', 'Ancona', 'ITA', '43.616666666666670', '13.360277777777778'),
(128, 'LI03', 'Alfina', 'Castel Viscardo', 'ITA', '42.733333333333334', '11.966666666666667'),
(129, 'LIQS', 'Ampugnano', 'Siena', 'ITA', '43.258611111111110', '11.255000000000000'),
(130, 'LICJ', 'Punta Raisi', 'Palermo', 'ITA', '38.181944444444440', '13.099444444444446'),
(131, 'LIQB', 'Arezzo', 'Arezzo', 'ITA', '43.455833333333340', '11.846944444444444'),
(132, 'LI17', 'Baialupo', 'Baialupo', 'ITA', '45.553333333333330', '9.505555555555556'),
(133, 'LIDB', 'Belluno', 'Belluno', 'ITA', '46.167222222222220', '12.247777777777777'),
(134, 'LILI', 'Vercelli', 'Vercelli', 'ITA', '45.311111111111110', '8.417499999999999'),
(135, 'LIKH', 'Avro', 'Rivoli', 'ITA', '46.235833333333330', '13.073333333333332'),
(136, 'LIRQ', 'Peretola', 'Florence', 'ITA', '43.808611111111105', '11.202777777777778'),
(137, 'LIEO', 'Costa Smeralda', 'Olbia', 'ITA', '40.898611111111110', '9.517777777777779'),
(138, 'LI13', 'Masera', 'Masera', 'ITA', '46.135833333333330', '8.310000000000000'),
(139, 'LI18', 'Pratello', 'Peccioli', 'ITA', '43.554166666666670', '10.752500000000000'),
(140, 'LIED', 'Decimomannu', 'Decimomannu', 'ITA', '39.353850000000000', '8.971725000000000'),
(141, 'LIPM', 'Marzaglia', 'Modena', 'ITA', '44.634722222222220', '10.810277777777780'),
(142, 'LI47', 'Grecciano', 'Livorno', 'ITA', '43.628611111111110', '10.482777777777779'),
(143, 'LIQL', 'Tassignano', 'Lucca', 'ITA', '43.829722222222220', '10.578888888888889'),
(144, 'LIPC', 'Cervia', 'Cervia', 'ITA', '44.221766666666670', '12.317561111111111'),
(145, 'LIER', 'Fenosu', 'Oristano', 'ITA', '39.894999999999996', '8.643055555555556'),
(146, 'LIPA', 'Aviano AB', 'Aviano', 'ITA', '46.031077777777774', '12.596463888888890'),
(147, 'LI09', 'Francavilla Bisio', 'Francavilla Bisio', 'ITA', '44.730555555555554', '8.730555555555556'),
(148, 'LIDF', 'Fano', 'Fano', 'ITA', '43.825833333333335', '13.027500000000002'),
(149, 'LIPH', 'S.Angelo', 'Treviso', 'ITA', '45.650833333333330', '12.197777777777778'),
(150, 'LIDR', 'Ravenna', 'Ravenna', 'ITA', '44.364444444444445', '12.224722222222223'),
(151, 'LILH', 'Rivanazzano', 'Voghera', 'ITA', '44.960277777777780', '9.009722222222223'),
(152, 'LI07', 'Costa D''Argento', 'Costa D''Argento', 'ITA', '42.495277777777780', '11.239444444444443'),
(153, 'LICD', 'Lampedusa', 'Lampedusa', 'ITA', '35.498055555555560', '12.618333333333334'),
(154, 'LIPK', 'Forli', 'Forli', 'ITA', '44.195555555555550', '12.069722222222222'),
(155, 'LI05', 'Ceresara', 'Ceresara', 'ITA', '45.264722222222225', '10.583333333333334');

-- --------------------------------------------------------

--
-- Struttura della tabella `configurazioni`
--

CREATE TABLE `configurazioni` (
  `nome` varchar(64) NOT NULL PRIMARY KEY,
  `valore` varchar(255) NOT NULL
);

--
-- Dump dei dati per la tabella `configurazioni`
--

INSERT INTO `configurazioni` (`nome`, `valore`) VALUES
('cognome', ''),
('inizializzato', '0'),
('nome', '');
