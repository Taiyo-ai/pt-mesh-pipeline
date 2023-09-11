from tqdm import tqdm
import unicodedata
import re


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

    new_sector = []
    new_sub_sector = []

    for i, row in project_data.iterrows():
        new_sector.append([])
        new_sub_sector.append([])
        sector = row["sector"].lower()

        try:
            subsector = row["sub_sector"].lower()
        except Exception as e:
            subsector = row["subsector"].lower()

        if sector == "transport":
            new_sector[i].append("transport")

            if subsector == "airports and aviation infrastructure":
                new_sub_sector[i].append("aviation")
            elif subsector == "inland waterways":
                new_sub_sector[i].append("port")
            elif subsector == "ports":
                new_sub_sector[i].append("water transport")
            elif (
                subsector == "railway rolling stock"
                or subsector == "railway terminal infrastructure"
                or subsector == "railway track"
            ):
                new_sub_sector[i].append("railways")
            elif subsector == "roads & bridges":
                new_sub_sector[i].append("roads")
            elif subsector == "urban public transport":
                new_sub_sector[i].append("administration")
            else:
                new_sub_sector[i].append("other")
        elif sector == "water & sanitation":
            if subsector == "irrigation":
                new_sector[i].append("agriculture")
                new_sub_sector[i].append("irrigation and drainage")
            elif subsector == "sewage collection, treatment and disposal":
                new_sector[i].append("water, sanitation and waste management")
                new_sub_sector[i].append("sanitation and sewerage")
            elif subsector == "solid waste management":
                new_sector[i].append("water, sanitation and waste management")
                new_sub_sector[i].append("muncipal waste")
            elif subsector == "storm water drainage system":
                new_sector[i].append("water, sanitation and waste management")
                new_sub_sector[i].append("muncipal waste")
            elif subsector == "water treatment plants":
                new_sector[i].append("water, sanitation and waste management")
                new_sub_sector[i].append("sanitation and sewerage")
            else:
                new_sector[i].append("water, sanitation and waste management")
                new_sub_sector[i].append("other")

        elif sector == "tourism":
            new_sector[i].append("industry, trade and services")
            new_sub_sector[i].append("tourism")

        elif sector == "social-infrastructure":
            if subsector == "medical infrastructure":
                new_sector[i].append("health")
                new_sub_sector[i].append("construction and facility")
            else:
                new_sector[i].append("industry, trade and services")
                new_sub_sector[i].append("infrastructure")

        elif sector == "retail":
            new_sector[i].append("industry, trade and services")
            new_sub_sector[i].append("trade")

        elif sector == "real-estate":
            if subsector == "commercial real estate":
                new_sector[i].append("industry, trade and services")
                new_sub_sector[i].append("industry and development")
            elif subsector == "industry related parks / zones":
                new_sector[i].append("industry, trade and services")
                new_sub_sector[i].append("urban and rural development")
            elif subsector == "public space development":
                new_sector[i].append("industry, trade and services")
                new_sub_sector[i].append("urban and rural development")
            elif subsector == "residential real estate (excl. affordable housing)":
                new_sector[i].append("industry, trade and services")
                new_sub_sector[i].append("housing")

        elif sector == "pharma,-biotech-and-lifesciences":
            new_sector[i].append("health")
            new_sub_sector[i].append("medicine")

        elif sector == "oil-and-gas":
            new_sector[i].append("energy and extractives")
            new_sub_sector[i].append("oil and gas")

        elif sector == "manufacturing":
            new_sector[i].append("industry, trade and services")
            new_sub_sector[i].append("manufacturing")

        elif sector == "logistics":
            new_sector[i].append("transport")
            new_sub_sector[i].append("other")

        elif sector == "information-technology":
            if subsector == "data centers":
                new_sector[i].append("ict")
                new_sub_sector[i].append("data center")
            elif subsector == "it & bpm":
                new_sector[i].append("ict")
                new_sub_sector[i].append("administration")
            elif subsector == "software solutions":
                new_sector[i].append("ict")
                new_sub_sector[i].append("infrastructure")

        elif sector == "food-processing-and-agriculture":
            if subsector == "food processing & additives":
                new_sector[i].append("agriculture")
                new_sub_sector[i].append("agribusiness")
            elif subsector == "horticulture & livestock":
                new_sector[i].append("agriculture")
                new_sub_sector[i].append("livestock")

        elif sector == "energy":
            if subsector == "electricity distribution":
                new_sector[i].append("energy and extractives")
                new_sub_sector[i].append("transmission and distribution")
            elif subsector == "electricity generation (non-renewable)":
                new_sector[i].append("energy and extractives")
                new_sub_sector[i].append("non-renewable")
            elif subsector == "electricity generation (renewable)":
                new_sector[i].append("energy and extractives")
                new_sub_sector[i].append("renewable")
            elif subsector == "electricity transmission":
                new_sector[i].append("energy and extractives")
                new_sub_sector[i].append("transmission and distribution")
            elif subsector == "oil/gas/lng storage":
                new_sector[i].append("energy and extractives")
                new_sub_sector[i].append("oil and gas")

        elif sector == "communication":
            new_sector[i].append("ict")
            new_sub_sector[i].append("telecommunication")

        elif sector == "commercial infrastructure":
            new_sector[i].append("industry, trade and services")
            new_sub_sector[i].append("infrastructure")

        elif sector == "bfsi":
            new_sector[i].append("financial")
            new_sub_sector[i].append("banking")

        elif sector == "automotive":
            new_sector[i].append("industry, trade and services")
            new_sub_sector[i].append("manufacturing")

        elif sector == "csr":
            if subsector == "education":
                new_sector[i].append("education")
                new_sub_sector[i].append("other")
            elif subsector == "environment":
                new_sector[i].append("environment")
                new_sub_sector[i].append("environmental protection")
            elif subsector == "healthcare & wellness":
                new_sector[i].append("health")
                new_sub_sector[i].append("other")
            elif subsector == "rural development":
                new_sector[i].append("industry, trade and services")
                new_sub_sector[i].append("urban and rural development")
            elif subsector == "skill development":
                new_sector[i].append("education")
                new_sub_sector[i].append("workforce devlopment/skills")
            elif "sports":
                new_sector[i].append("industry, trade and services")
                new_sub_sector[i].append("infrastructure")
            elif subsector == "technology incubators":
                new_sector[i].append("ict")
                new_sub_sector[i].append("administration")
            elif sector == "water & sanitation":
                new_sector[i].append("water, sanitation and waste management")
                new_sub_sector[i].append("sanitation and sewerage")
            else:
                new_sector[i].append("other")
                new_sub_sector[i].append("other")
    project_data["identified_sector"] = new_sector
    project_data["identified_subsector"] = new_sub_sector

    sec_sub_sec_tupple = []
    for i in range(project_data.shape[0]):
        temp = []
        for j in range(len(project_data.iloc[i, -2])):
            temp.append((project_data.iloc[i, -2][j], project_data.iloc[i, -1][j]))
        sec_sub_sec_tupple.append(temp)

    project_data["identified_sector_subsector_tuple"] = sec_sub_sec_tupple

    return project_data


# Combine all columns containing raw data under the name: 'raw_text'
def extract_textual_info(project_data, columns):
    cols = columns
    obj_cols = list(project_data.select_dtypes(include=["object"]).columns)
    obj_cols = [i for i in obj_cols if i in cols]
    obj_cols = [i for i in obj_cols if "id" not in i and "date" not in i]
    obj_cols = [i for i in obj_cols if "start" not in i and "end" not in i]

    project_data["raw_text"] = project_data[obj_cols].apply(
        lambda x: " ".join([str(i) for i in x.tolist()]), axis=1
    )
    project_data["raw_text"] = (
        project_data["raw_text"]
        .replace("NIL", "", regex=True)
        .replace("nan", "", regex=True)
    )
    return project_data


def preprocess_sentence(sentence: str):
    sentence = unicode_to_ascii(sentence.lower().strip())
    # replacing email addresses with blank space
    sentence = re.sub(
        r"[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z]{2,5}", " ", sentence
    )
    # replacing urls with blank space
    sentence = re.sub(
        r"\bhttp:\/\/([^\/]*)\/([^\s]*)|https:\/\/([^\/]*)\/([^\s]*)", " ", sentence
    )
    sentence = sentence.strip()
    return sentence


def unicode_to_ascii(s):
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )


def generate_raw_text(project_data, cols):
    project_data = extract_textual_info(project_data, cols)
    project_data["raw_text"] = project_data["raw_text"].apply(preprocess_sentence)
    return project_data
