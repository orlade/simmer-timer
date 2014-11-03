from util import ROOT, dict_to_list, call


def cityLanguage_calls():
    cmd = 'java -cp /opt/h2/bin/h2-1.4.182.jar org.h2.tools.Shell -url ' \
          'jdbc:h2:/opt/h2-data/world -sql'.split() + ['''
              SELECT language, percentage FROM countrylanguage WHERE
              countrycode = (SELECT countrycode FROM city WHERE name = '%s')
              ORDER BY percentage DESC LIMIT 1;''' % 'Melbourne']

    return [cmd]


def cityLanguage():
    return call(cityLanguage_calls()[0])
