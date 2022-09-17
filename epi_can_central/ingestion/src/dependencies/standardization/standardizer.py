from tqdm import tqdm


def sector_sub_sector_update(project_data, column):

    """
    This class does a keyword search and maps the keys to likely appropriate
    sector and subsector. May not be the most accurate and efficient method but
    good for a general higher level view.

    Parameters:
        project_data: pandas dataframe with sector and sub sector columns
        column: the column to be considered for identification

    returns:
        pandas dataframe
    """

    project_data[column] = project_data[column].apply(lambda x: str(x).lower())
    new_sector = []
    new_sub_sector = []

    for i, sector in tqdm(enumerate(project_data[column])):
        new_sector.append([])
        new_sub_sector.append([])

        ######  Agriculture   ############################
        if "fish" in sector:
            new_sector[i].append("agriculture")
            new_sub_sector[i].append("fisheries")

        if (
            "crop" in sector
            or "grain" in sector
            or "fruits" in sector
            or "vegetable" in sector
            or "sugarcane" in sector
            or "cotton" in sector
        ):
            new_sector[i].append("agriculture")
            new_sub_sector[i].append("crops")

        if (
            "agribusiness" in sector
            or "breweries" in sector
            or "agroindustry" in sector
            or "storage" in sector
        ):
            if "apartment" in sector:
                pass
            else:
                new_sector[i].append("agriculture")
                new_sub_sector[i].append("agribusiness")

        if (
            "coffee" in sector
            or "cocoa" in sector
            or "tea" in sector
            or "horti" in sector
        ):
            new_sector[i].append("agriculture")
            new_sub_sector[i].append("crops")

        if "forest" in sector:
            new_sector[i].append("agriculture")
            new_sub_sector[i].append("forestry")

        if "livestock" in sector or "animal" in sector or "poultry" in sector:
            new_sector[i].append("agriculture")
            new_sub_sector[i].append("livestock")

        if (
            "irrigation" in sector
            or "drainage" in sector
            or ("agri" in sector and "flood" in sector)
            or "natural resources management" in sector
        ):
            new_sector[i].append("agriculture")
            new_sub_sector[i].append("irrigation and drainage")

        if "dairy" in sector or "cattle" in sector:
            new_sector[i].append("agriculture")
            new_sub_sector[i].append("dairy")

        if (
            "agriculture" in sector or "agricultural" in sector or "agro" in sector
        ) and "admin" in sector:
            new_sector[i].append("agriculture")
            new_sub_sector[i].append("administration")

        if "fertilizer" in sector:
            new_sector[i].append("agriculture")
            new_sub_sector[i].append("fertilizer")

        if "wineries" in sector or "sugar and confectionery" in sector:
            if "apartment" in sector:
                pass
            else:
                new_sector[i].append("agriculture")
                new_sub_sector[i].append("agribusiness")

        if "farm products" in sector or "grocery" in sector or "food" in sector:
            if "apartment" in sector:
                pass
            else:
                new_sector[i].append("agriculture")
                new_sub_sector[i].append("agribusiness")

        if (
            "agriculture" in sector
            or "agricultural" in sector
            or "agro" in sector in sector
        ):
            if len(new_sector[i]) == 0:
                new_sector[i].append("agriculture")
                new_sub_sector[i].append("other")

        ####### Energy ##################
        if ("energy" in sector or "electricity" in sector) and (
            "transmission" in sector or "distribution" in sector
        ):
            new_sector[i].append("energy and extractives")
            new_sub_sector[i].append("transmission and distribution")

        if (
            "distribution and transmission" in sector
            or "power" in sector
            or "heating" in sector
            or "energy utility" in sector
            or ("highway" in sector and "energy" in sector)
            or "electrification" in sector
            or "electric substation" in sector
        ):
            new_sector[i].append("energy and extractives")
            new_sub_sector[i].append("transmission and distribution")

        if "efficiency" in sector:
            new_sector[i].append("energy and extractives")
            new_sub_sector[i].append("efficiency and conservation")

        if (
            "electricity generation" in sector
            or "electricity" in sector
            or "watt" in sector
        ):
            new_sector[i].append("energy and extractives")
            new_sub_sector[i].append("electricity generation")

        if (
            "oil" in sector
            or "gas" in sector
            or "fuel" in sector
            or "refining" in sector
            or "petrochemical" in sector
            or "petroleum" in sector
        ):
            new_sector[i].append("energy and extractives")
            new_sub_sector[i].append("oil and gas")

        if "hydro" in sector:
            new_sector[i].append("energy and extractives")
            new_sub_sector[i].append("hydro")

        if "solar" in sector:
            new_sector[i].append("energy and extractives")
            new_sub_sector[i].append("solar")

        if "wind" in sector:
            new_sector[i].append("energy and extractives")
            new_sub_sector[i].append("wind")

        if "biomass" in sector or "bioenergy" in sector:
            new_sector[i].append("energy and extractives")
            new_sub_sector[i].append("biomass")

        if "thermal" in sector or "heating" in sector:
            new_sector[i].append("energy and extractives")
            new_sub_sector[i].append("thermal")

        if "geothermal" in sector:
            new_sector[i].append("energy and extractives")
            new_sub_sector[i].append("geothermal")

        if (
            "renewable" in sector
            or "conventional" in sector
            or "waste to energy" in sector
            or "lowcarbon" in sector
            or "clean energy" in sector
        ):
            new_sector[i].append("energy and extractives")
            new_sub_sector[i].append("renewable")

        if "coal" in sector and "energy" in sector and not "non" in sector:
            new_sector[i].append("energy and extractives")
            new_sub_sector[i].append("non-renewable")

        if "energy" in sector and "admin" in sector:
            new_sector[i].append("energy and extractives")
            new_sub_sector[i].append("administration")

        if (
            "gold" in sector
            or "aluminum" in sector
            or "tungsten" in sector
            or "copper" in sector
            or "diamonds" in sector
        ):
            new_sector[i].append("energy and extractives")
            new_sub_sector[i].append("mining")

        if (
            "quar" in sector
            or "nickel" in sector
            or "gypsum" in sector
            or "silver" in sector
            or "zinc" in sector
            or "coal" in sector
        ):
            new_sector[i].append("energy and extractives")
            new_sub_sector[i].append("mining")

        if "energy" in sector:
            if len(new_sector[i]) == 0:
                new_sector[i].append("energy and extractives")
                new_sub_sector[i].append("other")

        ###### health ###########
        if (
            "health" in sector
            and ("construction" in sector or "facility" in sector)
            or "hospital" in sector
            or "nursing" in sector
            or "clinic" in sector
        ):
            new_sector[i].append("health")
            new_sub_sector[i].append("construction and facility")

        if "health" in sector and "admin" in sector:
            new_sector[i].append("health")
            new_sub_sector[i].append("administration")

        if (
            "health" in sector
            and (
                "system development" in sector
                or "mother" in sector
                or "child" in sector
            )
            or "care" in sector
            or "health programs" in sector
        ):
            new_sector[i].append("health")
            new_sub_sector[i].append("healthcare services")

        if "nutrition" in sector:
            new_sector[i].append("health")
            new_sub_sector[i].append("disease prevention and control")

        if "disease" in sector:
            new_sector[i].append("health")
            new_sub_sector[i].append("disease prevention and control")

        if (
            ("pharmaceuticals" and "medicine" in sector)
            or "medi" in sector
            or "pharmaceutical" in sector
        ):
            new_sector[i].append("health")
            new_sub_sector[i].append("medicine")

        if "health" in sector:
            if len(new_sector[i]) == 0:
                new_sector[i].append("health")
                new_sub_sector[i].append("other")

        ########### transport ##################
        if (
            "waterway" in sector
            or ("water" in sector and "transport" in sector)
            or "harbor" in sector
            or " port" in sector
        ):
            if (
                "export" in sector
                or "import" in sector
                or "support" in sector
                or "airport" in sector
                or "sports" in sector
                or "surface transport" in sector
            ):
                pass
            else:
                new_sector[i].append("transport")
                new_sub_sector[i].append("ports/waterways")

        if (
            "ports" in sector
            or "ship building and repairing" in sector
            or "marine" in sector
        ):
            if (
                "export" in sector
                or "import" in sector
                or "support" in sector
                or "airport" in sector
                or "sports" in sector
                or "surface transport" in sector
            ):
                pass
            else:
                new_sector[i].append("transport")
                new_sub_sector[i].append("ports/waterways")

        if (
            "aviation" in sector
            or ("air" in sector and "transport" in sector)
            or "airport" in sector
        ):
            new_sector[i].append("transport")
            new_sub_sector[i].append("aviation")

        if "railway" in sector or "train" in sector or "rail" in sector:
            if "training" in sector or "light" in sector:
                pass
            else:
                new_sector[i].append("transport")
                new_sub_sector[i].append("railways")

        if (
            "road" in sector
            or "highway" in sector
            or "logging" in sector
            or "tunnel" in sector
            or "bridge" in sector
            or "motorway" in sector
        ):
            new_sector[i].append("transport")
            new_sub_sector[i].append("roads")

        if "transport" in sector and "admin" in sector:
            new_sector[i].append("transport")
            new_sub_sector[i].append("administration")

        if "urban mobility" in sector:
            new_sector[i].append("transport")
            new_sub_sector[i].append("administration")

        if "passenger" in sector or "sidewalk" in sector or "parking lot" in sector:
            new_sector[i].append("transport")
            new_sub_sector[i].append("services")

        if "freight" in sector:
            new_sector[i].append("transport")
            new_sub_sector[i].append("services")

        if "bus and heavy commercial vehicle" in sector:
            new_sector[i].append("transport")
            new_sub_sector[i].append("services")

        if "transport" in sector:
            if len(new_sector[i]) == 0:
                new_sector[i].append("transport")
                new_sub_sector[i].append("other")

        ############# Education ###########
        if (
            "workforce development" in sector
            or "skill" in sector
            or "vocation" in sector
            or "training" in sector
        ):
            new_sector[i].append("education")
            new_sub_sector[i].append("workforce devlopment/skills")

        if "school" in sector:
            if "primary school" in sector:
                pass
            else:
                new_sector[i].append("education")
                new_sub_sector[i].append("secondary education")

        if "college" in sector or "universi" in sector:
            new_sector[i].append("education")
            new_sub_sector[i].append("tertiary education")

        if (
            "childhood development" in sector
            or "university" in sector
            or "primary school" in sector
        ):
            new_sector[i].append("education")
            new_sub_sector[i].append("childhood education")

        if "education" in sector:
            if "tertiary" in sector or "higher" in sector:
                new_sector[i].append("education")
                new_sub_sector[i].append("tertiary education")
            elif "secondary" in sector:
                new_sector[i].append("education")
                new_sub_sector[i].append("secondary education")
            elif "primary" in sector:
                new_sector[i].append("education")
                new_sub_sector[i].append("primary education")
            elif "childhood" in sector:
                new_sector[i].append("education")
                new_sub_sector[i].append("childhood education")
            elif (
                "adult" in sector
                or "basic" in sector
                or "continuing" in sector
                or "nonformal education" in sector
                or "compensatory" in sector
            ):
                new_sector[i].append("education")
                new_sub_sector[i].append("adult, basic or continuing education")
            elif "admin" in sector or "institution" in sector:
                new_sector[i].append("education")
                new_sub_sector[i].append("administration")
            elif "research" in sector:
                new_sub_sector[i].append("research")
                new_sector[i].append("education")
            else:
                if len(new_sector[i]) == 0:
                    new_sector[i].append("education")
                    new_sub_sector[i].append("other")

        ####### Financial ###########
        if "bank" in sector and not "non" in sector:
            new_sector[i].append("financial")
            new_sub_sector[i].append("banking")

        if "preinvestment" in sector:
            new_sector[i].append("financial")
            new_sub_sector[i].append("banking")

        if ("non" in sector and "bank" in sector) or "noninvestment" in sector:
            new_sector[i].append("financial")
            new_sub_sector[i].append("non-bank finance")

        if "insurance" in sector or "pension" in sector:
            new_sector[i].append("financial")
            new_sub_sector[i].append("insurance and pension")

        if "capital market" in sector or (
            (
                "equity" in sector
                or "debt" in sector
                or "investment" in sector
                or "portfolio" in sector
                or "capital" in sector
            )
            and "fund" in sector
        ):
            new_sector[i].append("financial")
            new_sub_sector[i].append("capital market")

        if (
            "credit lines" in sector
            or "loans" in sector
            or "lending" in sector
            or "small business fund" in sector
            or "mortgage" in sector
            or "fund" in sector
        ):
            new_sector[i].append("financial")
            new_sub_sector[i].append("credit lines/loan")

        if (
            ("financial" in sector or "finance" in sector)
            and "admin" in sector
            or "privatization" in sector
            or "remittance" in sector
            or "regulation and supervision" in sector
        ):
            new_sector[i].append("financial")
            new_sub_sector[i].append("administration")

        if (
            "agricultural markets" in sector or "agricultural credit" in sector
        ) or "extension" in sector:
            new_sector[i].append("financial")
            new_sub_sector[i].append("agricultural markets")

        if "economic management" in sector or "consumer" in sector:
            new_sector[i].append("financial")
            new_sub_sector[i].append("administration")

        if "payment" in sector or "inclus" in sector:
            new_sector[i].append("financial")
            new_sub_sector[i].append("services")

        if (
            "distressed assets" in sector
            or "decentralization" in sector
            or "credit information services" in sector
            or "credit reporting and secured transactions" in sector
        ):
            new_sector[i].append("financial")
            new_sub_sector[i].append("administration")

        if (
            "mutual fund" in sector
            or "exchanges (trading systems)" in sector
            or "fund management" in sector
            or "derivatives (includes risk management entities)" in sector
            or "leasing" in sector
        ):
            new_sector[i].append("financial")
            new_sub_sector[i].append("capital market")

        if "financial" in sector or "finance" in sector:
            if len(new_sector[i]) == 0:
                new_sector[i].append("financial")
                new_sub_sector[i].append("other")

        ####### water, sanitation and waste management ############
        if (
            "sanitation" in sector
            or "sewerage" in sector
            or ("sanit" in sector and "water" in sector)
            or "sewer" in sector
        ):
            new_sector[i].append("water, sanitation and waste management")
            new_sub_sector[i].append("sanitation and sewerage")

        if ("water" in sector and "supply" in sector) or "water" in sector:
            new_sector[i].append("water, sanitation and waste management")
            new_sub_sector[i].append("supply")

        if "water" in sector and "admin" in sector:
            new_sector[i].append("water, sanitation and waste management")
            new_sub_sector[i].append("administration")

        if (
            "water" in sector and "waste" in sector
        ) or "sewage treatment plant" in sector:
            new_sector[i].append("water, sanitation and waste management")
            new_sub_sector[i].append("sanitation and sewerage")

        if "waste" in sector:
            if "solid" in sector or "municipal" in sector:
                new_sector[i].append("water, sanitation and waste management")
                new_sub_sector[i].append("muncipal waste")
            if "water" in sector or "liquid" in sector:
                new_sector[i].append("water, sanitation and waste management")
                new_sub_sector[i].append("liquid waste")
            else:
                if len(new_sector[i]) == 0:
                    new_sector[i].append("water, sanitation and waste management")
                    new_sub_sector[i].append("other")

        ###### industry , trade and services ########
        if (
            "housing" in sector
            or "house" in sector
            or "residential building" in sector
            or "resident" in sector
            or "apartment" in sector
            or "dormitory" in sector
        ):
            if "warehouse" in sector:
                pass
            else:
                new_sector[i].append("industry, trade and services")
                new_sub_sector[i].append("housing")

        if (
            ("urban" in sector and "development" in sector)
            or "modernization" in sector
            or "urban developm" in sector
            or "urban management" in sector
            or "rural" in sector
            or "light" in sector
            or "lighting" in sector
        ):
            new_sector[i].append("industry, trade and services")
            new_sub_sector[i].append("urban and rural development")

        if (
            "building" in sector
            and "residential" in sector
            and not "non" in sector
            or "home" in sector
        ):
            new_sector[i].append("industry, trade and services")
            new_sub_sector[i].append("housing")

        if "building" in sector:
            new_sector[i].append("industry, trade and services")
            new_sub_sector[i].append("urban and rural development")

        if (
            "fabric mills" in sector
            or "finishing (dyeing, printing, finishing, etc.)" in sector
        ):
            new_sector[i].append("industry, trade and services")
            new_sub_sector[i].append("manufacturing")

        if "broker/dealer" in sector or "distribution business" in sector:
            new_sector[i].append("industry, trade and services")
            new_sub_sector[i].append("trade")

        if "manufacturing" in sector:
            new_sector[i].append("industry, trade and services")
            new_sub_sector[i].append("manufacturing")

        if (
            "industry" in sector
            or "trade" in sector
            or "services" in sector
            or "industries" in sector
        ) and "administration" in sector:
            new_sector[i].append("industry, trade and services")
            new_sub_sector[i].append("administration")

        if (
            "tourism" in sector
            or "tour" in sector
            or "amusement park" in sector
            or "travel" in sector
        ):
            new_sector[i].append("industry, trade and services")
            new_sub_sector[i].append("tourism")

        if "hotel" in sector or "motel" in sector:
            new_sector[i].append("industry, trade and services")
            new_sub_sector[i].append("hotel")

        if "mining" in sector:
            new_sector[i].append("industry, trade and services")
            new_sub_sector[i].append("mining")

        if (
            "sme" in sector
            or "small scale enterprise" in sector
            or "industrial" in sector
            or "enterprise" in sector
            or "industries" in sector
            or "sector development" in sector
        ):
            new_sector[i].append("industry, trade and services")
            new_sub_sector[i].append("industry and development")

        if (
            "trade" in sector
            or "sugar and confectionery" in sector
            or "b2c" in sector
            or "sales" in sector
            or "mall" in sector
        ):
            new_sector[i].append("industry, trade and services")
            new_sub_sector[i].append("trade")

        if "industry" in sector or "commercial" in sector:
            new_sector[i].append("industry, trade and services")
            new_sub_sector[i].append("industry and development")

        if (
            "rental" in sector
            or "packaging" in sector
            or "printing" in sector
            or "postal" in sector
            or "service" in sector
        ):
            if "govern" in sector:
                pass
            else:
                new_sector[i].append("industry, trade and services")
                new_sub_sector[i].append("services")

        if (
            "aerospace product and parts" in sector
            or "cement" in sector
            or "concrete pipes" in sector
            or "garment and apparel" in sector
            or "furniture" in sector
            or "ceramic tiles" in sector
            or "glass products" in sector
            or "bricks" in sector
            or "coated products" in sector
        ):
            new_sector[i].append("industry, trade and services")
            new_sub_sector[i].append("manufacturing")

        if (
            "alkalies and chlorine" in sector
            or "chemical" in sector
            or "carbon black" in sector
        ):
            new_sector[i].append("industry, trade and services")
            new_sub_sector[i].append("chemical")

        if "agency reform" in sector:
            new_sector[i].append("industry, trade and services")
            new_sub_sector[i].append("administration")

        if "automotive" in sector:
            new_sector[i].append("industry, trade and services")
            new_sub_sector[i].append("manufacturing")

        if (
            "wood products" in sector
            or "sawmilling" in sector
            or "spinning" in sector
            or "switch" in sector
            or "soft drink" in sector
            or "paper" in sector
            or "paint" in sector
            or "plastic" in sector
            or "soap" in sector
            or "shoes" in sector
            or "steel" in sector
            or "pipelines" in sector
            or "mill" in sector
            or "ceramic" in sector
            or "pottery" in sector
            or "metal" in sector
            or "nylon" in sector
            or "iron" in sector
            or "motor" in sector
        ):

            if "environ" in sector:
                pass
            else:
                new_sector[i].append("industry, trade and services")
                new_sub_sector[i].append("manufacturing")

        if (
            "utilities" in sector
            or "arena" in sector
            or "stadium" in sector
            or "office" in sector
            or "entertainment" in sector
        ):
            if "environ" in sector or "water" in sector or "social safety" in sector:
                pass
            else:
                new_sector[i].append("industry, trade and services")
                new_sub_sector[i].append("infrastructure")

        if "fitness" in sector or "sports" in sector or "recreation center":
            if "environ" in sector or "water" in sector or "social safety" in sector:
                pass
            else:
                new_sector[i].append("industry, trade and services")
                new_sub_sector[i].append("infrastructure")

        if "infrastructure" in sector:
            if "environ" in sector or "water" in sector or "social safety" in sector:
                pass
            else:
                new_sector[i].append("industry, trade and services")
                new_sub_sector[i].append("infrastructure")

        if "composite infrastructure" in sector or "construction" in sector:
            if "environ" in sector or "water" in sector:
                pass
            else:
                new_sector[i].append("industry, trade and services")
                new_sub_sector[i].append("infrastructure")

        ###### ICT ############
        if (
            ("ict" in sector or "information and communications technolog" in sector)
            and "services" in sector
            or "broadband" in sector
        ):
            new_sector[i].append("ict")
            new_sub_sector[i].append("services")

        if (
            ("ict" in sector or "information and communications technolog" in sector)
            and "infrastructure" in sector
            or "it enabled services" in sector
        ):
            new_sector[i].append("ict")
            new_sub_sector[i].append("infrastructure")

        if (
            "ict" in sector or "information and communications technolog" in sector
        ) and "administration" in sector:
            new_sector[i].append("ict")
            new_sub_sector[i].append("administration")

        if "computer systems design and related services" in sector:
            new_sector[i].append("ict")
            new_sub_sector[i].append("infrastructure")

        if "electrical machinery" in sector:
            new_sector[i].append("ict")
            new_sub_sector[i].append("infrastructure")

        if (
            ("tele" in sector)
            or "mobile" in sector
            or "internet" in sector
            or "communication" in sector
        ):
            new_sector[i].append("ict")
            new_sub_sector[i].append("telecommunication")

        if "information vendor" in sector:
            new_sector[i].append("ict")
            new_sub_sector[i].append("administration")

        if "data center" in sector or "data centre" in sector:
            new_sector[i].append("ict")
            new_sub_sector[i].append("data center")

        if "ict" in sector or "information and communication" in sector:
            if len(new_sector[i]) == 0:
                new_sector[i].append("ict")
                new_sub_sector[i].append("other")

        ###### social #############
        if "social" in sector and "admin" in sector:
            new_sector[i].append("social protection")
            new_sub_sector[i].append("administration")

        if (
            "social" in sector
            and ("investment" in sector or "service" in sector)
            or "nondepository" in sector
        ):
            new_sector[i].append("social protection")
            new_sub_sector[i].append("investment/service")

        if "labor" in sector or "employ" in sector:
            new_sector[i].append("social protection")
            new_sub_sector[i].append("investment/service")

        if (
            "social protection" in sector
            or "compensatory" in sector
            or "social safety" in sector
        ):
            new_sector[i].append("social protection")
            new_sub_sector[i].append("programmes, schemes and safety measures")

        if "social" in sector:
            if len(new_sector[i]) == 0:
                new_sector[i].append("social protection")
                new_sub_sector[i].append("other")

        ########## natural disaster/environment and tech ################
        if "flood protection" in sector or "flood control" in sector:
            new_sector[i].append("environment")
            new_sub_sector[i].append("disastor management")

        if "disaster" in sector:
            new_sector[i].append("environment")
            new_sub_sector[i].append("disastor management")

        if (
            "environment" in sector
            or "natural resources" in sector
            or "pollution" in sector
        ):
            new_sector[i].append("environment")
            new_sub_sector[i].append("environmental protection")

        if "research" in sector or "science and technology" in sector:
            new_sector[i].append("science and technology and research")
            new_sub_sector[i].append("science and technology and research")

        if "multi" in sector and "sector" in sector:
            new_sector[i].append("multi sector")
            new_sub_sector[i].append("multi sector")

        ####### Public Administration ############
        if (
            "central" in sector
            and "government" in sector
            or "regional integration" in sector
        ):
            new_sector[i].append("public administration")
            new_sub_sector[i].append("central government")

        if "sub-national" in sector and "government" in sector:
            new_sector[i].append("public administration")
            new_sub_sector[i].append("sub-national government")

        if "civil service reform" in sector or "economic management" in sector:
            new_sector[i].append("public administration")
            new_sub_sector[i].append("central government")

        if "subnational" in sector:
            new_sector[i].append("public administration")
            new_sub_sector[i].append("sub-national government")

        if (
            "aids" in sector
            or "com signatory" in sector
            or "government services" in sector
        ):
            new_sector[i].append("public administration")
            new_sub_sector[i].append("public sector management")

        if (
            "public" in sector
            and "management" in sector
            or "institutional development" in sector
            or "capacity development" in sector
        ):
            new_sector[i].append("public administration")
            new_sub_sector[i].append("public sector management")

        if "law" in sector or "policy" in sector or "adjustment" in sector:
            new_sector[i].append("public administration")
            new_sub_sector[i].append("laws and policies")

        if (
            "justice" in sector
            or "judiciary" in sector
            or "judicial" in sector
            or "justice" in sector
        ):
            new_sector[i].append("public administration")
            new_sub_sector[i].append("judiciary")

        if "public administration" in sector:
            if len(new_sector[i]) == 0:
                new_sector[i].append("public administration")
                new_sub_sector[i].append("other")

    ####### Modifications ############
    project_data["identified_sector"] = new_sector
    project_data["identified_subsector"] = new_sub_sector

    sec_sub_sec_tupple = []
    for i in range(project_data.shape[0]):
        temp = []
        for j in range(len(project_data.iloc[i, -2])):
            temp.append((project_data.iloc[i, -2][j], project_data.iloc[i, -1][j]))
        sec_sub_sec_tupple.append(temp)

    project_data["identified_sector_subsector_tuple"] = sec_sub_sec_tupple
    project_data.drop(columns=[column], inplace=True)

    return project_data
