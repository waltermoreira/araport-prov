from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from prov.model import ProvDocument, Namespace, Literal, PROV, Identifier, ProvAgent
import datetime
import pydot
import prov.dot

def example():

    g = ProvDocument()
    # Local namespace
    # Doesnt exist yet so we are creating it
    ap = Namespace('aip', 'https://araport.org/provenance/')
    # Dublin Core
    g.add_namespace("dcterms", "http://purl.org/dc/terms/")
    # FOAF
    g.add_namespace("foaf", "http://xmlns.com/foaf/0.1/")

    # Add sponsors and contributors as Agents
    # ap['matthew_vaughn']
    # aip:matthew_vaughn
    # https://araport.org/provenance/:matthew_vaughn
    me = g.agent(ap['matthew_vaughn'], {
        'prov:type': PROV["Person"], 'foaf:givenName': "Matthew Vaughn", 'foaf:mbox': "<mailto:vaughn@tacc.utexas.edu>"
    })
    walter = g.agent(ap['walter_moreira'], {
        'prov:type': PROV["Person"], 'foaf:givenName': "Walter Moreira", 'foaf:mbox': "<mailto:wmoreira@tacc.utexas.edu>"
    })
    utexas = g.agent(ap['university_of_texas'], {
        'prov:type': PROV["Organization"], 'foaf:givenName': "University of Texas at Austin"
    })

    # Include the ADAMA platform as an Agent and set attribution
    adama_platform = g.agent(ap['adama_service'], {'dcterms:title': "ADAMA", 'dcterms:description': "Araport Data and Microservices API", 'dcterms:language':"en-US", 'aip:uri':"https://api.araport.org/community/v0.3/" })
    g.wasGeneratedBy(adama_platform, walter)
    # Set delegation to our host University
    g.actedOnBehalfOf(walter, utexas)

    # Include the ADAMA microservice as an Agent and set attribution+delegation
    adama_microservice = g.agent(ap['adama_service'], {'dcterms:title': "BAR Annotation Service", 'dcterms:description': "Returns annotation from locus ID", 'dcterms:language':"en-US", 'aip:uri':"https://api.araport.org/community/v0.3/mwvaughn/bar_annotation_v1.0.0" })
    g.wasGeneratedBy(adama_microservice, me, datetime.datetime.now())
    g.actedOnBehalfOf(me, utexas)

    # Describe the relationship between the microservice and the platform
    g.used(adama_microservice, adama_platform, datetime.datetime.now())

    # Sources
    # U Toronto BAR provided by Nick Provart
    # Agents
    nick = g.agent(ap['nicholas_provart'], {
        'prov:type': PROV["Person"], 'foaf:givenName': "Nicholas Provart"
    })
    utoronto = g.agent(ap['university_of_toronto'], {
        'prov:type': PROV["Organization"], 'foaf:givenName': "University of Toronto"
    })
    g.actedOnBehalfOf(nick, utoronto)
    # Define source as Entity
    # dcterms:language: Recommended best practice is to use a controlled vocabulary such as RFC 4646
    datasource1 = g.entity(ap['datasource1'], {'dcterms:title': "BAR Arabidopsis AGI -> Annotation", 'dcterms:description': "Most recent annotation for given AGI", 'dcterms:language':"en-US", 'aip:uri':"http://bar.utoronto.ca/webservices/agiToAnnot.php"})
    # Set up attribution to Nick
    g.wasGeneratedBy(datasource1, nick)

    # TAIR, general
    # Agents
    # dcterms:language: Recommended best practice is to use a controlled vocabulary such as RFC 4646
    eva = g.agent(ap['eva_huala'], {
        'prov:type': PROV["Person"], 'foaf:givenName': "Eva Huala"
    })
    phoenix = g.agent(ap['phoenix_bioinformatics'], {
        'prov:type': PROV["Organization"], 'foaf:givenName': "Phoenix Bioinformatics"
    })
    g.actedOnBehalfOf(eva, phoenix)
    # Define source as Entity
    datasource2 = g.entity(ap['datasource2'], {'dcterms:title': "TAIR", 'dcterms:description': "The Arabidopsis Information Resource", 'dcterms:language':"en-US", 'aip:uri':"https://www.arabidopsis.org/" })
    g.wasGeneratedBy(datasource2, eva)

    # In Sources.yml, these two sources are nested. Define that relationship here
    g.wasDerivedFrom(ap['datasource1'], ap['datasource2'])

    # Define all valid ADAMA types as activities
    # Eventually, break these into more atomic actions in a chain
    action1 = g.activity(ap['process_query'], datetime.datetime.now())
    # action1 = g.activity(ap['process_map'], datetime.datetime.now())
    # action1 = g.activity(ap['process_generic'], datetime.datetime.now())
    # action1 = g.activity(ap['process_passthrough'], datetime.datetime.now())
    # Future... Native microservices
    # action1 = g.activity(ap['generate'], datetime.datetime.now())

    # Define current ADAMA response as an Entity
    # This is what's being returned to the user and is thus the subject of the PROV record
    # May be able to add more attributes to it but this is the minimum
    response = g.entity(ap['adama_response'])

    # Response is generated by the process_query action
    g.wasGeneratedBy(response, ap['process_query'])
    # The process_query used the microservice
    g.used(ap['process_query'], adama_microservice)
    # The microservice used datasource1
    g.used(adama_microservice, datasource1)

    # Print prov_n
    print(g.prov_n)
    # Print prov-json
    print(g.serialize())
    # Write out as a pretty picture
    graph = prov.dot.prov_to_dot(g)
    graph.write_png('Sources.png')

}