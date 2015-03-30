import random


def slogan():
    slogans = ['student success', 'fiscal stability', 'student achievement', 'community satisfaction']
    variable = random.choice(slogans)

    data = {
        "variable": variable
    }

    return data


def article():
    articles = [
        ['"Ypsilanti Community Schools graduates inaugural senior class."',
         'http://www.mlive.com/news/ann-arbor/index.ssf/2014/06/ypsilanti_community_schools_gr.html',
         '- Amy Biolchini', 'MLive | 6/03/2014', '61'],
        ['"Ypsilanti schools to pursue college scholarship program similar to Kalamazoo Promise."',
         'http://www.annarbor.com/news/ypsilanti/ypsilanti-community-schools-to-pursue-college-scholarship-program-'
         'similar-to-kalamazoo-promise/',
         '- Danielle Arndt', 'The Ann Arbor News | 7/25/2013', '85'],
        ['"Ypsilanti New Tech High School sends off its inaugural graduating class."',
         'http://www.heritage.com/articles/2014/05/23/ypsilanti_courier/news/doc537f84b324c9c781733383.txt',
         '- Krystal Elliott', 'The Ypsilanti Courier | 5/23/2014', '74'],
        ['"State Superintendent Mike Flanagan says school district deficits \'reducing\' overall."',
         'http://www.mlive.com/lansing-news/index.ssf/2014/06/flanagan_deficit_districts.html',
         '- Brian Smith', 'MLive | 6/08/2014', '86'],
        ['"Ypsilanti schools authorizes restructuring $18.8M debt to no longer be a deficit district."',
         'http://www.annarbor.com/news/ypsilanti/ypsilanti-schools-authorizes-restructuring-its-188m-debt-to-no-'
         'longer-be-a-deficit-district/',
         '- Danielle Arndt', 'The Ann Arbor News | 6/26/2013', '92'],
    ]

    article_snip = random.choice(articles)

    data = {
        'title': article_snip[0],
        'link': article_snip[1],
        'author': article_snip[2],
        'journal': article_snip[3],
        'length': article_snip[4]
    }

    return data


def article2():
    articles = [
        ['"Year-round school? Ypsilanti schools considering expanding use of balanced calendar."',
         'http://www.mlive.com/news/ann-arbor/index.ssf/2014/08/ypsilanti_schools_to_consider.html',
         '- Amy Biolchini', 'MLive | 8/09/2014', '86'],
        ['"Holmes Elementary School starts off strong as first to pilot balanced calendar in Ypsilanti Community '
         'Schools."',
         'http://www.heritage.com/articles/2014/08/21/ypsilanti_courier/news/doc53f61a1be160f522813720.txt',
         '- Krystal Elliott', 'The Ypsilanti Courier | 8/21/2014', '112'],
        ['"City officials propose stationing police officer at Ypsilanti Community Middle School."',
         'http://www.heritage.com/articles/2014/06/17/ypsilanti_courier/news/doc53a054c6786f5399518913.txt',
         '- Krystal Elliott', 'The Ypsilanti Courier | 6/17/2014', '88'],
        ['"Ypsilanti teachers, district \'satisfied\' overall with union contract despite some concerns over '
         'salaries."',
         'http://www.heritage.com/articles/2014/09/17/ypsilanti_courier/news/doc541221141ab45551957933.txt',
         '- Krystal Elliott', 'The Ypsilanti Courier | 9/17/2014', '106'],
        ['"Ypsilanti Community Schools Adopts Elementary Reconfiguration Plan."',
         'http://wemu.org/post/ypsilanti-community-schools-adopts-elementary-reconfiguration-plan',
         '- Bob Eccles', 'WEMU 89.1 | 4/22/2014', '68']
        ]

    article_snip = random.choice(articles)

    data = {
        'title': article_snip[0],
        'link': article_snip[1],
        'author': article_snip[2],
        'journal': article_snip[3],
        'length': article_snip[4]
    }

    return data