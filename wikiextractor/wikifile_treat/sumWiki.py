import shutil

wiki_AA = open('/home/daniela/wiki_pagelinks_2016-10/wikipedia20180401/wikiextractor/result_wikiextractor_1/AA', 'w')
for file in ['wiki_00', 'wiki_01', 'wiki_02', 'wiki_03', 'wiki_04', 'wiki_05', 'wiki_06', 'wiki_07', 'wiki_08',
             'wiki_09', 'wiki_10', 'wiki_11', 'wiki_12', 'wiki_13', 'wiki_14', 'wiki_15', 'wiki_16', 'wiki_17',
             'wiki_18', 'wiki_19' 'wiki_20', 'wiki_21', 'wiki_22', 'wiki_23', 'wiki_24', 'wiki_25', 'wiki_26',
             'wiki_27', 'wiki_28', 'wiki_29', 'wiki_30', 'wiki_31', 'wiki_32', 'wiki_33', 'wiki_34', 'wiki_35',
             'wiki_36', 'wiki_37', 'wiki_38', 'wiki_39', 'wiki_40', 'wiki_41', 'wiki_42', 'wiki_43', 'wiki_44',
             'wiki_45', 'wiki_46', 'wiki_47', 'wiki_48', 'wiki_49', 'wiki_50', 'wiki_51', 'wiki_52', 'wiki_53',
             'wiki_54', 'wiki_55', 'wiki_56', 'wiki_57', 'wiki_58', 'wiki_59', 'wiki_60', 'wiki_61', 'wiki_62',
             'wiki_63', 'wiki_64', 'wiki_65', 'wiki_66', 'wiki_67', 'wiki_68', 'wiki_69', 'wiki_70', 'wiki_71',
             'wiki_72', 'wiki_73', 'wiki_74', 'wiki_75', 'wiki_76', 'wiki_77', 'wiki_78', 'wiki_79', 'wiki_80',
             'wiki_81', 'wiki_82', 'wiki_83', 'wiki_84', 'wiki_85', 'wiki_86', 'wiki_87', 'wiki_88', 'wiki_89',
             'wiki_9', 'wiki_91', 'wiki_92', 'wiki_93', 'wiki_94', 'wiki_95', 'wiki_96', 'wiki_97', 'wiki_98',
             'wiki_99']:
    with open(file, 'r') as infile:
        # wiki_AA.write(infile.read())
        shutil.copyfileobj(infile, wiki_AA)
