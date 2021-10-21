# Create your views here.
import pandas as pd
import json
import os
from django.shortcuts import render
from django.http import JsonResponse
from .forms import Myform
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

dir_name = "static/coursefinder/csv/"
# filname = "coursefinder_2.xlsx"
# path = os.path.join(dir_name, filname)
major_cities = {
    "Canada": ["Montreal", "Vancouver", "Toronto", "Ottawa", "Quebec City"],
    "United Kingdom": ["London", "Edinburgh", "Manchester", "Birmingham", "Glasgow"],
    "United Arab Emirates": ["Dubai", "Abu Dhabi", "Sharjah", "Al Ain", "Ajman"],
    "Australia": ["Sydney", "	Melbourne", "Brisbane", "Perth", "Adelaide"],
    "France": ["Paris", "Lyon", "Marseille", "Toulouse", "Lille-Roubaix"],
    "Germany": ["Berlin", "Hamburg", "Munich", "Cologne", "Frankfurt", "am main"],
    "USA": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
    "Netherlands": [
        "Amsterdam",
        "Rotterdam",
        "The Hague",
        "Utrecht",
        "Eindhoven",
    ],
    "Malaysia": [
        "Kuala Lumpur",
        "George Town",
        "Ipoh",
        "Johor Bahru",
        "Malacca",
    ],
    "Hong Kong": [
        "Kowloon",
        "Tsuen Wan",
        "yuen long kau hui",
        "Tung Chung",
        "Shatin",
    ],
    "Ireland": [
        "Dublin",
        "Galway",
        "Belfast",
        "Limerick",
        "Kilkenny",
    ],
    "New Zealand": [
        "Auckland",
        "Christchurch",
        "Wellington",
        "Hamilton",
        "Tauranga",
    ],
    "Singapore": [
        "Bedok",
        "Jurong West",
        "Tampines",
        "Woodlands",
        "Sengkang",
    ],
    "Sweden": [
        "Stockholm",
        "Gothenburg",
        "Malmo",
        "Uppsala",
        "Vasteras",
    ],
}

collegesheet = pd.read_csv(
    os.path.join(dir_name, "college.csv"), encoding="unicode_escape"
)
coursesheet_1 = pd.read_csv(
    os.path.join(dir_name, "coursepart1.csv"), encoding="unicode_escape", low_memory=False
)

coursesheet_2 = pd.read_csv(
    os.path.join(dir_name, "coursepart2.csv"), encoding="unicode_escape", low_memory=False
)
coursesheet = coursesheet_1.append(coursesheet_2,ignore_index=True)
dropdownData = pd.read_csv(
    os.path.join(dir_name, "dropdownData.csv"),
    encoding="unicode_escape",
    low_memory=False,
)
dropdownData['country_id'] = dropdownData['country_id'].astype('int')
dropdownData['new_sub_streamsID'] = dropdownData['new_sub_streamsID'].astype('int')
dropdownData['head2ID'] = dropdownData['head2ID'].astype('int')
country_map = dropdownData[['country','country_id']].drop_duplicates().dropna()
country_map['country_id'] = country_map['country_id'].astype('int')


levelfile = coursesheet[["levelID", "degree_type"]].drop_duplicates()
levelfile["parent_id"] = 0

leveldata = levelfile.rename(columns={"levelID": "id", "degree_type": "name"}).to_dict(
    "records"
)


country_dict = {}
for key in major_cities.keys():
    country_dict[key] = pd.read_csv(f"{dir_name}/countries/{key}.csv")

consultant_col = ["Krishna Consultant", "Applyboard", "AEC Consultant"]
ranking_col = [
    "QS World",
    "US NEWS Global",
    "THE",
]
fees_col = [
    "tuition_fees_per_year",
    "living_cost_per_year",
    "total_tuition_fees",
    "total_living_cost",
]
course_columns = [
    "head_one",
    "head_two",
    "deadline",
    "estimated_LOA_TAT",
    "eligibility",
    "new_sub_streams",
    "degree_type",
    "head_short_form",
    "course_duration_value",
    "total_fees",
    "consultant",
    "course_duration",
    "Program_name",
    "streamID",
    "levelID",
    "tution_living_per_year",
]
eligibility_col = ["Gmat", "TOEFL", "IELTS", "GRE", "SAT"]
datafile = coursesheet.merge(collegesheet, on="college_id", how="left")
datafile.drop_duplicates(inplace=True)


def convert_tostring(x):
    if x <= 99999:
        val = round(x / 1000, 1)
        val = f"{val}K"
    elif (x > 99999) and (x <= 9999999):
        val = round(x / 100000, 1)
        val = f"{val}L"

    else:
        val = round(x / 10000000, 1)
        val = f"{val}cr"

    return val


# @app.route('/coursefinder/form')
def index(request):
    form = Myform()
    if request.method == "POST":
        
        stream_id = request.POST.getlist("Stream")
        level_id = request.POST.getlist("Level")
        substream_id = request.POST.getlist("substream")
        country_id = request.POST["Country"]

        print(datafile.dtypes)

        streamFilter = datafile["new_sub_streamsID"].isin(map(int,stream_id))
        
        levelFilter = datafile["levelID"].isin(map(int,level_id))
        
        headFilter  = datafile['head2ID'].isin(map(int,substream_id))
        
        print(datafile[streamFilter & levelFilter  & headFilter])
        country_name = country_map[country_map["country_id"] == int(country_id)]['country'].values[0]
        country_filter = datafile['country_id']==int(country_id)
        
        
        filtered_data = datafile[streamFilter & levelFilter  & headFilter & country_filter]
        # print(filtered_data.shape[0])
        d_context = {"message": ""}
        if filtered_data.shape[0] == 0:
            d_context[
                "message"
            ] = f"The course you are looking for is not available for {country_name}, try another"
            return render(request, "coursefinder/coursefinderResult.html", d_context)

        country_data = country_dict[country_name].drop(["city"], axis=1)
        # country_data['city_id'] = country_data['city_id'].astype('int')
        filtered_data = filtered_data.merge(country_data, on="city_id", how="left")
        s = filtered_data["total_fees"]
        res = pd.qcut(s, 5, duplicates="drop")

        cats = res.cat.categories
        fees_bins_df = pd.DataFrame(columns=["id", "text", "min", "max"])
        minimum = cats.left.to_list()
        maximum = cats.right.to_list()
        length = len(minimum)
        for i in range(length):
            if i == 0:
                fees_bins_df.loc[i, "id"] = 1
                fees_bins_df.loc[i, "text"] = f"<{convert_tostring(maximum[i])}"
                fees_bins_df.loc[i, "min"] = 0
                fees_bins_df.loc[i, "max"] = maximum[i]

            elif i + 1 == length:
                fees_bins_df.loc[i, "id"] = length
                fees_bins_df.loc[i, "text"] = f">{convert_tostring(minimum[i])}"
                fees_bins_df.loc[i, "min"] = minimum[i]
                fees_bins_df.loc[i, "max"] = maximum[i]

            else:
                fees_bins_df.loc[i, "id"] = i + 1
                fees_bins_df.loc[
                    i, "text"
                ] = f"{convert_tostring(minimum[i])}-{convert_tostring(maximum[i])}"
                fees_bins_df.loc[i, "min"] = minimum[i]
                fees_bins_df.loc[i, "max"] = maximum[i]

        distance_from = major_cities[country_name]

        filtered_data["ranking_dict"] = filtered_data[ranking_col].to_dict("records")
        filtered_data["distance_dict"] = filtered_data[distance_from].to_dict("records")
        filtered_data["deadline"] = filtered_data["deadline"].apply(
            lambda x: json.loads(x)
        )
        filtered_data["consultant"] = filtered_data[consultant_col].to_dict("records")

        filtered_data["eligibility"] = filtered_data[eligibility_col].to_dict("records")
        # print(filtered_data.columns)

        filtered_data["tution_living_per_year"] = (
            filtered_data["tuition_fees_per_year"]
            + filtered_data["living_cost_per_year"]
        )
        # filtered_data['tution_living_total'] = filtered_data['total_tuition_fees']+filtered_data['total_living_cost']

        file = (
            filtered_data.groupby("college_id")[course_columns]
            .apply(lambda x: x.to_dict("records"))
            .reset_index()
        )

        file.columns = ["college_id", "course_info"]
        filtered_data_unique = filtered_data.drop_duplicates(
            ["college_id"], keep="first"
        )

        filtered_data = filtered_data_unique.merge(file, on="college_id", how="left")

        filtered_data.sort_values(["search_volume"], inplace=True, ascending=False)
        # filtered_data = filtered_data[filtered_data['Partner']!=1]
        partner_colleges = filtered_data[filtered_data["Partner"] == 1].to_dict("records")

        filtered_dict = filtered_data.to_dict("records")
        degree = filtered_data[[col for col in ["head_short_form"] for i in range(2)]]

        degree.columns = ["id", "name"]
        degree = degree[degree.id != "-"]

        institute_type = filtered_data[[col for col in ["institute_type"] for i in range(2)]]
        institute_type.columns = ["id", "name"]
        institute_type = institute_type[institute_type.id != "-"]

        user_filters = {
            "college_filter": filtered_data[["college_id", "college_name"]]
            .dropna()
            .drop_duplicates()
            .rename(columns={"college_id": "id", "college_name": "name"})
            .to_dict("records"),
            "level_filter": filtered_data[["streamID", "Program_name"]]
            .dropna()
            .drop_duplicates()
            .rename(columns={"streamID": "id", "Program_name": "name"})
            .to_dict("records"),
            "fees_filters": fees_bins_df.to_dict("records"),
            "degree_filters": degree.dropna()
            .drop_duplicates()
            .to_dict("records"),
            "institute_type_filters": institute_type.dropna()
            .drop_duplicates()
            .to_dict("records"),
            
            "city_state": filtered_data[["city_state_id", "city_state"]]
            .dropna()
            .drop_duplicates()
            .rename(columns={"city_state_id": "id", "city_state": "name"})
            .to_dict("records"),
            "ranking_filtes": ranking_col,
            "exam_filtes": eligibility_col,
            "consultant_filtes": consultant_col,
            "ielts_filters": [
                {"id": 1, "text": " < 5", "max": 5},
                {"id": 2, "text": " 5 - 6", "max": 6, "min": 5},
                {"id": 3, "text": "6 - 7", "max": 7, "min": 6},
                {"id": 4, "text": " > 7", "min": 7},
            ],
        }

        dropcol = consultant_col + eligibility_col + ranking_col + course_columns
        filtered_data.drop(dropcol, axis=1, inplace=True)

        d_context = {
            "filtered_dict": filtered_dict,
            "user_filters": user_filters,
            "partner_colleges": partner_colleges,
        }
        return render(request, "coursefinder/coursefinderResult.html", d_context)
    return render(
        request,
        "coursefinder/cascadingform.html",
        {"form": form},
    )



# @app.route('coursefinder/levelbins/7lq2x')
def levellist(request):
    leveldict = levelfile.dropna().to_dict("records")
    return JsonResponse(leveldict, safe=False)

@csrf_exempt
def streamlist(request):
    dropdown_datadict = {}
    if request.method == "POST":
        # print(request.POST)
        if (
            ("typeid[]" in request.POST)
            and ("Streamid[]" in request.POST)
            and ("substreamid[]" in request.POST)
            
        ):
            level_id = request.POST.getlist("typeid[]")
            
            level_filter = dropdownData["levelID"].isin(list(map(int, level_id)))
            stream_id = request.POST.getlist("Streamid[]")
            print()
            stream_filter = dropdownData["new_sub_streamsID"].isin(list(map(int, stream_id)))
            substream_id = request.POST.getlist("substreamid[]")
           
            substream_filter = (
                dropdownData["head2ID"].isin(list(map(int, substream_id)))
            )

            dropdown_data = dropdownData[
                level_filter & stream_filter & substream_filter
            ][["country", "country_id"]].drop_duplicates()
            
            dropdown_data.rename(
                columns={"country_id": "id", "country": "text"}, inplace=True
            )
            dropdown_datadict = dropdown_data.to_dict("records")

        elif (
            ("typeid[]" in request.POST)
            and ("Streamid[]" in request.POST)
            and ("substreamid[]" in request.POST)
           
        ):
            level_id = request.POST.getlist("typeid[]")
            
            level_filter = dropdownData["levelID"].isin(list(map(int, level_id)))
            stream_id = request.POST.getlist("Streamid[]")
            print()
            stream_filter = dropdownData["new_sub_streamsID"].isin(list(map(int, stream_id)))
            substream_id = request.POST.getlist("substreamid[]")
            country_filter = dropdownData["country"]
            substream_filter = (
                dropdownData["head2ID"].isin(list(map(int, substream_id)))
            )

            dropdown_data = dropdownData[
                level_filter & stream_filter & substream_filter 
            ][["country", "country_id"]].drop_duplicates()
            
            dropdown_data.rename(
                columns={"country_id": "id", "country": "text"}, inplace=True
            )
            dropdown_datadict = dropdown_data.to_dict("records")        
        
        elif ("typeid[]" in request.POST) and ("Streamid[]" in request.POST) and "name" in request.POST:
            level_id = request.POST.getlist("typeid[]")
            name = request.POST.get("name")
            level_filter = dropdownData["levelID"].isin(list(map(int, level_id)))
            stream_id = request.POST.getlist("Streamid[]")
            stream_filter = dropdownData["new_sub_streamsID"].isin(list(map(int, stream_id)))
            head2_filter = dropdownData["head2"].str.contains(name, case=False)
            dropdown_data = dropdownData[level_filter & stream_filter & head2_filter][
                ["head2", "head2ID","course_rating"]
            ].drop_duplicates().sort_values(by=["course_rating"])

            dropdown_data.rename(
                columns={"head2ID": "id", "head2": "text"}, inplace=True
            )
            dropdown_datadict = dropdown_data[["id","text"]].to_dict("records")

        elif ("typeid[]" in request.POST) and ("Streamid[]" in request.POST) and "name" not in request.POST:
            level_id = request.POST.getlist("typeid[]")
            level_filter = dropdownData["levelID"].isin(list(map(int, level_id)))
            stream_id = request.POST.getlist("Streamid[]")
            stream_filter = dropdownData["new_sub_streamsID"].isin(list(map(int, stream_id)))

            dropdown_data = dropdownData[level_filter & stream_filter][
                ["head2", "head2ID","course_rating"]
            ].drop_duplicates().sort_values(by=["course_rating"])

            dropdown_data.rename(
                columns={"head2ID": "id", "head2": "text"}, inplace=True
            )
            dropdown_datadict = dropdown_data[["id","text"]].to_dict("records")
        elif request.POST.__contains__("typeid[]") and "name" in request.POST:
            level_id = request.POST.getlist("typeid[]")
            name = request.POST.get("name")

            level_filter = dropdownData["levelID"].isin(list(map(int, level_id)))
            new_sub_streams = dropdownData['new_sub_streams'].str.contains(name, case=False)
            dropdown_data = dropdownData[level_filter & new_sub_streams][
                ["new_sub_streams", "new_sub_streamsID","stream_rating"]
            ].drop_duplicates().sort_values(by=["stream_rating"])

            dropdown_data.rename(
                columns={"new_sub_streamsID": "id", "new_sub_streams": "text"},
                inplace=True,
            )
            dropdown_datadict = dropdown_data[["id","text"]].to_dict("records")

        elif request.POST.__contains__("typeid[]") and "name" not in request.POST:
            level_id = request.POST.getlist("typeid[]")
            

            level_filter = dropdownData["levelID"].isin(list(map(int, level_id)))

            dropdown_data = dropdownData[level_filter][
                ["new_sub_streams", "new_sub_streamsID","stream_rating"]
            ].drop_duplicates().sort_values(by=["stream_rating"])

            dropdown_data.rename(
                columns={"new_sub_streamsID": "id", "new_sub_streams": "text"},
                inplace=True,
            )
            dropdown_datadict = dropdown_data[["id","text"]].to_dict("records")

        else:

            dropdown_data = dropdownData[["levelID", "degree_type"]].drop_duplicates()
            dropdown_data.rename(
                columns={"levelID": "id", "degree_type": "text"}, inplace=True
            )
            dropdown_datadict = dropdown_data.to_dict("records")

    return JsonResponse(dropdown_datadict, safe=False)

