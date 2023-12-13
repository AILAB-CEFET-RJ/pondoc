import pyparsing
from .reader import read_publications

from pyparsing import (Word, 
                       Literal, 
                       OneOrMore, 
                       alphanums, 
                       printables, 
                       alphas8bit,
                       nums,
                       ZeroOrMore)


def makeDecoratingParseAction(marker):
    def parse_action_impl(s,l,t):
        return (marker, t)
    return parse_action_impl

def parse_publication_remainder(citation_str, debug = False):
    conference_name = (Literal('EM: ') | Literal('Em: ')).suppress() + OneOrMore(Word(printables+alphas8bit+u'º'+u'ª', excludeChars='.,'), stopOn=Literal('.'))
    conference_name = conference_name.setParseAction(makeDecoratingParseAction("conference_name"))

    page_indicator = Literal('p.')
    page_indicator = page_indicator.setParseAction(makeDecoratingParseAction("page_indicator"))

    volume_indicator = Literal('v.')
    volume_indicator = volume_indicator.setParseAction(makeDecoratingParseAction("volume_indicator"))

    valid_year = Word(nums, exact=4) + Literal('.').suppress()
    publication_year = (valid_year | Literal('0') + Literal('.').suppress())
    publication_year = publication_year.setParseAction(makeDecoratingParseAction("year"))

    # see https://stackoverflow.com/questions/59106516/pyparsing-for-unicode-letters
    journal_name1 = OneOrMore(Word(printables+alphas8bit), stopOn=volume_indicator) + volume_indicator.suppress() + page_indicator.suppress()
    journal_name2 = OneOrMore(Word(printables+alphas8bit), stopOn=volume_indicator) + volume_indicator.suppress()
    journal_name3 = OneOrMore(Word(printables+alphas8bit), stopOn=page_indicator) + page_indicator.suppress()
    journal_name = (journal_name1 | journal_name2 | journal_name3)
    # journal_name = OneOrMore(Word(unicodePrintables), stopOn=volume_indicator)
    journal_name = journal_name.setParseAction(makeDecoratingParseAction("journal_name"))
    
    conference_or_journal_name = (conference_name | journal_name)
    conference_or_journal_name = conference_or_journal_name.setParseAction(makeDecoratingParseAction("conference_or_journal_name"))

    remaining_stuff = ZeroOrMore(Word(printables+alphas8bit), stopOn=publication_year)
    remaining_stuff = remaining_stuff.setParseAction(makeDecoratingParseAction("Remaining"))

    valid_qualis = (Word(alphanums, exact=2) | Literal('C')) + ZeroOrMore(Word(printables, excludeChars='.'))

    unindentified_qualis = Literal('NÃO IDENTIFICADO') | Literal('Não identificado')
    ni_qualis =  (unindentified_qualis + OneOrMore(Word(printables+alphas8bit+u'º'+u'ª', excludeChars='.')))

    qualis = (valid_qualis | ni_qualis + Literal('.').suppress())
    qualis = qualis.setParseAction(makeDecoratingParseAction("qualis"))

    if debug:
        # to track the matching expressions
        conference_name.setName("conference_name").setDebug()
        journal_name.setName("journal_name").setDebug()
        conference_or_journal_name.setName("conference_or_journal_name").setDebug()
        publication_year.setName("year").setDebug()
        volume_indicator.setName("volume_indicator").setDebug()
        remaining_stuff.setName("Remaining").setDebug()
        qualis.setName("qualis").setDebug()
    
    citation = (Literal('.') + 
                conference_or_journal_name + 
                remaining_stuff +
                publication_year +
                qualis)

    result = citation.parseString(citation_str)

    return result

def infosCitation(result):
    if result is None:
        return None
    authors = []
    for element in result.asList():
        if element[0] == 'author':
            try: authors.append(element[1][0][1].asList() + element[1][1][1].asList())
            except: authors.append(element[1].asList())
        elif element[0] == 'title':
            title = element[1].asList()
            title = ' '.join(word for word in title)
        elif element[0] == 'conference_or_journal_name':
            conference_journal = element[1].asList()
            conference_journal = conference_journal[0][1]
            conference_journal = ' '.join(word for word in conference_journal)
        elif element[0] == 'Remaining':
            remaining = element[1].asList()
            remaining = ' '.join(word for word in remaining)
            if 'issn' in remaining:                
                l = remaining.find('issn: ') + 6
                issn = remaining[l:l+9]
        elif element[0] == 'year':
            year = element[1][0]
        elif element[0] == 'qualis':
            qualis = element[1].asList()
            qualis = ' '.join(word for word in qualis)

    try: return conference_journal, issn, year, qualis
    except: return conference_journal, year, qualis

def formatString(x: str):
    return x

def parsePublication(citation, debug = False):
    authors = citation[0]
    authors = authors.split(";")
    authors = [formatString(author).split(',') for author in authors]
    publication_title = formatString(citation[1])
    citation_details = formatString(citation[2])
    try:
        citation_details_parsing_result = parse_publication_remainder(citation_details, debug)
    except pyparsing.exceptions.ParseException as e:
        print(f"Parsing error on publication '{citation_details}': {e}.")
        citation_details_parsing_result = None
        raise e
    return (authors, publication_title, infosCitation(citation_details_parsing_result))


if __name__ == "__main__":
    beginYear = 2022
    endYear = 2023
    infosp, infosa, infosc = read_publications(beginYear, endYear)
    for ano in range(beginYear, endYear+1):
        citations = infosp[ano]
        for citation in citations:
            authors, publication_title, other_publication_details = parsePublication(citation)
            print(authors)
            print(publication_title)
            print(other_publication_details)
            print()

        #ignorar infosa!

        citations = infosc[ano]
        for citation in citations:
            print(f"Current publication: {citation}")
            authors, publication_title, other_publication_details = parsePublication(citation, False)
            print(authors)
            print(publication_title)
            print(other_publication_details)
            print()
