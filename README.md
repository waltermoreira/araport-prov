# Implementing Provenance in ADAMA

Objective: Provide resource-level provenance for ADAMA microservices and thier source data

*Key notes from W3C PROV overview (http://www.w3.org/TR/prov-overview/)*

* PROV relations are named so they can be used in assertions about the past
* Physical, digital, conceptual things are called entities
* An entry's provenance may refer to other entities
* Activities are how entities come into existence and they are dynamic aspects of the world
* Activities are application specific and thus not defined by PROV (is this right??)
* Activities generate new entities
* Agents take a role in an activity such that the agent can be assigned responsibility for the activity taking place
* If an agent has responsibility for an activity it is said to be 'associated' with the activity
* Several agents may be associated with an activity. For example, the person and software involved in creating a chart are both agents. They are associated with 'creating' the 'chart'
* An agent can act on behalf of another. This allows us to say that Mary, an analyst at ACME Corp, was associated with creating a chart but that she was doing at her employer's behest.
* Another handy relationship for a data set is 'attributed to'. This is understood to mean that Entity A was directly responsible for generating Entity B. Example: Mary, from ACME Corp generated a chart using Stata. Generation of the chart is attributed to Mary acting on behalf of ACME and associated with Stata software.
* Roles describe the part played by an entity played in an activity. They also describe how agents participated in an activity. Roles are application specific and thus not defined by PROV.
* If existence of an entity (Mary's chart for instance) is due to another entity (a data set perhaps) then it is derived from that entity.
* Revision is a form of derivation
* Another special case of derivation is 'quoted from' indicating that the generated entity contains direct copy from the source entity. Example: Mary extracts a table from a Nature paper as part of a report she is writing. The provenance record for her report will indicate that she has 'quoted from' that Nature paper.
* Timestamps can describe when an entity was generated, or when an activity started and stopped
* Alternates allow entities referring to the same thing to be specified as alternates of one another
* Specializations allow one to refer to either revisions -or- to sub-sections of an entity. The latter will be a route we can use to tie prov records to the query made against a specific service.

Prefixes and Namespaces
* prov: The PROV ontology namespace
    * http://www.w3.org/ns/prov#
* dcterms: Dublin Core terms
    * http://semanticweb.org/wiki/Dublin_Core
    * http://purl.org/dc/terms/
* foaf: Friend of a Friend ontology
    * http://semanticweb.org/wiki/FOAF
    * http://xmlns.com/foaf/0.1/
* xsd: XSD namespace
    * http://www.w3.org/2001/XMLSchema#

## Implementation specifics

* Need a small controlled vocabulary of activity entities. This is not user-extensible in the prototype. These will all be in the private prefix aprov (for Araport Provenance). Can publish it as a formalized namespace in future
* Map 'activities' to ADAMA microservice types?
    * query : remap_query, query_source, transform_response, stream_result
    * map: remap_query, query_source, map_response, stream_result
    * generic: remap_query, query_source, map_response, return_result
    * passthough: retrieve, return_result
    * native: generate, stream_result
* Create a nestable list of sources in the service metadata (details TBD)

## What does a source look like?

* uri: Specific resource accessed by the ADAMA microservice. It can be any valid URI, including database connection strings. When supported, local file paths are relative to the service endpoint
* Proposed Dublin Core terms to support
    * title
    * description
    * bibliographicCitation
        * Plaintext, as per DC recommendation #2 (http://dublincore.org/documents/dc-citation-guidelines/)
    * language (https://www.ietf.org/rfc/rfc4646.txt)
    * license
    * modified
* sponsor_organization_name: Organization providing the service
* provider_name: Given name of responsible party (lab PI or other decision maker)
* sponsor_email: Email address for responsible party (optional)
* sources: List of contributing sources to the resource

{"title":"TAIR",
"description":"The Arabidopsis Information Resource",
"language":"en-us",
"sponsor_organization_name":"Phoenix Bioinformatics",
"uri":"https://www.arabidopsis.org/",
"sources":[]}

{"sources":[
    {"title":"BAR Arabidopsis AGI -> Annotation",
     "description":"Most recent annotation for given AGI",
     "language":"en-ca",
     "sponsor_organization_name":"University of Toronto",
     "provider_name":"Nicholas Provart",
     "uri":"http://bar.utoronto.ca/webservices/agiToAnnot.php",
     "sources":[
        {"title":"TAIR",
         "description":"The Arabidopsis Information Resource",
         "language":"en-us",
         "sponsor_organization_name":"Phoenix Bioinformatics",
         "uri":"https://www.arabidopsis.org/",
         "sources":[]}]}]}


## References

* http://www.w3.org/TR/prov-overview/
* http://www.w3.org/TR/prov-dm/
* http://prov.readthedocs.org/en/latest/
* https://github.com/trungdong/prov/blob/master/prov/tests/examples.py
* ProvToolbox (Java) https://lucmoreau.wordpress.com/2014/08/01/provtoolbox-tutorial-1-creating-and-saving-a-prov-document/
* http://dublincore.org/documents/2012/06/14/dcmi-terms/
* https://provenance.ecs.soton.ac.uk/prov-template/
* https://pythonhaven.wordpress.com/tag/pydot/
