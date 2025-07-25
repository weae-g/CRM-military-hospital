import pymorphy2


#region Падежи и соответсвующие

def get_accs_case(name):
    morph = pymorphy2.MorphAnalyzer()
    words = name.split()
    dative_forms = []
    for word in words:
        parsed_word = morph.parse(word)
        dative_form = [p.inflect({'accs'}).word.title() if word.istitle() else p.inflect({'accs'}).word for p in parsed_word if 'nomn' in p.tag]
        if dative_form:
            dative_forms.append(dative_form[0])
    return ' '.join(dative_forms)

def get_gent_case(name):
    morph = pymorphy2.MorphAnalyzer()
    words = name.split()
    dative_forms = []
    for word in words:
        parsed_word = morph.parse(word)
        dative_form = [p.inflect({'gent'}).word.title() if word.istitle() else p.inflect({'gent'}).word for p in parsed_word if 'nomn' in p.tag]
        if dative_form:
            dative_forms.append(dative_form[0])
    return ' '.join(dative_forms)

def get_ablt_case(name):
    morph = pymorphy2.MorphAnalyzer()
    words = name.split()
    dative_forms = []
    for word in words:
        parsed_word = morph.parse(word)
        dative_form = [p.inflect({'ablt'}).word.title() if word.istitle() else p.inflect({'ablt'}).word for p in parsed_word if 'nomn' in p.tag]
        if dative_form:
            dative_forms.append(dative_form[0])
    return ' '.join(dative_forms)

def get_loct_case(name):
    morph = pymorphy2.MorphAnalyzer()
    words = name.split()
    dative_forms = []
    for word in words:
        parsed_word = morph.parse(word)
        dative_form = [p.inflect({'loct'}).word.title() if word.istitle() else p.inflect({'loct'}).word for p in parsed_word if 'nomn' in p.tag]
        if dative_form:
            dative_forms.append(dative_form[0])
    return ' '.join(dative_forms)

def get_dative_case(full_name):
    morph = pymorphy2.MorphAnalyzer()
    words = full_name.split()
    dative_forms = []
    for word in words:
        parsed_word = morph.parse(word)
        dative_form = [p.inflect({'datv'}).word.title() if word.istitle() else p.inflect({'datv'}).word for p in parsed_word if 'nomn' in p.tag]
        if dative_form:
            dative_forms.append(dative_form[0])
    return ' '.join(dative_forms)

#endregion