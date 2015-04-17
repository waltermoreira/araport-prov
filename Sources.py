from __future__ import (absolute_import, division, print_function,
                    unicode_literals)

from prov.model import ProvDocument, Namespace, Literal, PROV, Identifier, ProvAgent
import datetime
import pydot, prov.dot
import json

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
    # Learn this from a call to profiles service? Adds a dependency on Agave so I am open to figuring out another way
    me = g.agent(ap['matthew_vaughn'], {
        'prov:type': PROV["Person"], 'foaf:givenName': "Matthew Vaughn", 'foaf:mbox': "<mailto:vaughn@tacc.utexas.edu>"
    })
    # Hard coded for now
    walter = g.agent(ap['walter_moreira'], {
        'prov:type': PROV["Person"], 'foaf:givenName': "Walter Moreira", 'foaf:mbox': "<mailto:wmoreira@tacc.utexas.edu>"
    })
    utexas = g.agent(ap['university_of_texas'], {
        'prov:type': PROV["Organization"], 'foaf:givenName': "University of Texas at Austin"
    })

    # Set delegation to our host University
    # We may have trouble doing this for other users since we don't always capture their host instituion
    g.actedOnBehalfOf(walter, utexas)
    g.actedOnBehalfOf(me, utexas)

    # Include the ADAMA platform as an Agent and set attribution
    # dcterms:title and dcterms:description are hardcoded
    # dcterms:language is hard-coded
    # dcterms:source is the URI of the public git source repository for ADAMA
    # "dcterms:updated": "2015-04-17T09:44:56" - this would actually be the date ADAMA was updated
    adama_platform = g.agent(ap['adama_service'], {'dcterms:title': "ADAMA", 'dcterms:description': "Araport Data and Microservices API", 'dcterms:language':"en-US", 'dcterms:identifier':"https://api.araport.org/community/v0.3/", 'dcterms:updated': "2015-04-17T09:44:56" })
    g.wasGeneratedBy(adama_platform, walter)

    # Include the ADAMA microservice as an Agent and set attribution+delegation
    # dcterms:title and dcterms:description are inherited from the service's metadata
    # dcterms:language is hard-coded
    # dcterms:identifier is the deployment URI for the service
    # dcterms:source is the URI of the public git source repository. The URL in this example is just a dummy
    adama_microservice = g.agent(ap['adama_service'], {'dcterms:title': "BAR Annotation Service", 'dcterms:description': "Returns annotation from locus ID", 'dcterms:language':"en-US", 'dcterms:identifier':"https://api.araport.org/community/v0.3/mwvaughn/bar_annotation_v1.0.0", 'dcterms:source':"https://github.com/Arabidopsis-Information-Portal/prov-enabled-api-sample" })

    # the microservice was generated by me on date X (don't use now, use when the service was updated)
    g.wasGeneratedBy(adama_microservice, me, datetime.datetime.now())
    # The microservice used the platform now
    g.used(adama_microservice, adama_platform, datetime.datetime.now())

    # Sources
    #
    # Define BAR
    # Agents
    nick = g.agent(ap['nicholas_provart'], {
        'prov:type': PROV["Person"], 'foaf:givenName': "Nicholas Provart", 'foaf:mbox': "provart@utoronta.ca"
    })
    utoronto = g.agent(ap['university_of_toronto'], {
        'prov:type': PROV["Organization"], 'foaf:givenName': "University of Toronto", 'dcterms:identifier':"http://www.utoronto.ca/"
    })
    g.actedOnBehalfOf(nick, utoronto)

    # Entity
    # All fields derived from Sources.yml
    # dcterms:title and dcterms:description come straight from the YAML
    # dcterms:identifier - URI pointing to the source's canonical URI representation
    # optional - dcterms:language: Recommended best practice is to use a controlled vocabulary such as RFC 4646
    # optional - dcterms:updated: date the source was published or last updated
    # optional - dcterms:license: Simple string or URI to license. Validate URI if provided?
    datasource1 = g.entity(ap['datasource1'], {'dcterms:title': "BAR Arabidopsis AGI -> Annotation", 'dcterms:description': "Most recent annotation for given AGI", 'dcterms:language':"en-US", 'dcterms:identifier':"http://bar.utoronto.ca/webservices/agiToAnnot.php", 'dcterms:updated':"2015-04-17T09:44:56", 'dcterms:license':"Creative Commons 3.0" })
    # Set up attribution to Nick
    g.wasAttributedTo(datasource1, nick)

    # Define TAIR
    # Agents
    # dcterms:language: Recommended best practice is to use a controlled vocabulary such as RFC 4646
    eva = g.agent(ap['eva_huala'], {
        'prov:type': PROV["Person"], 'foaf:givenName': "Eva Huala"
    })
    phoenix = g.agent(ap['phoenix_bioinformatics'], {
        'prov:type': PROV["Organization"], 'foaf:givenName': "Phoenix Bioinformatics"
    })
    g.actedOnBehalfOf(eva, phoenix)

    # Entity
    # All fields derived from Sources.yml
    # optional - dcterms:citation: Plain text bibliographic citation. If only provided as doi, should we try to validate it?
    datasource2 = g.entity(ap['datasource2'], {'dcterms:title': "TAIR", 'dcterms:description': "The Arabidopsis Information Resource", 'dcterms:language':"en-US", 'dcterms:identifier':"https://www.arabidopsis.org/", 'dcterms:citation':"The Arabidopsis Information Resource (TAIR): improved gene annotation and new tools. Nucleic Acids Research 2011 doi: 10.1093/nar/gkr1090"})
    g.wasAttributedTo(datasource2, eva)

    # In Sources.yml, these two sources are nested. Define that relationship here
    # There are other types of relationships but we will just use derived from for simplicity in this prototype
    g.wasDerivedFrom(ap['datasource1'], ap['datasource2'])

    # Depending on which ADAMA microservice type we are using, define an activity
    # Eventually, break these into more atomic actions in a chain
    action1 = g.activity(ap['do_query'], datetime.datetime.now())
    # action1 = g.activity(ap['do_map'], datetime.datetime.now())
    # action1 = g.activity(ap['do_generic'], datetime.datetime.now())
    # action1 = g.activity(ap['do_passthrough'], datetime.datetime.now())
    # Future... Support for ADAMA-native microservices
    # action1 = g.activity(ap['generate'], datetime.datetime.now())

    # Define current ADAMA response as an Entity
    # This is what's being returned to the user and is thus the subject of the PROV record
    # May be able to add more attributes to it but this is the minimum
    response = g.entity(ap['adama_response'])

    # Response is generated by the process_query action
    # Time-stamp it!
    g.wasGeneratedBy(response, ap['do_query'], datetime.datetime.now())
    # The process_query used the microservice
    g.used(ap['do_query'], adama_microservice, datetime.datetime.now())
    # The microservice used datasource1
    g.used(adama_microservice, datasource1, datetime.datetime.now())

    # Print prov_n
    print(g.get_provn())
    # Print prov-json
    print(g.serialize())
    # Write out as a pretty picture
    graph = prov.dot.prov_to_dot(g)
    graph.write_png('Sources.png')

