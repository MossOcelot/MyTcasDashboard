from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas
import styles

# from datas import province, api
from dash.long_callback import DiskcacheLongCallbackManager
import diskcache

df = pandas.read_csv("tcas_dataset_cleaned.csv")
df = df.drop(columns=["Unnamed: 0"])

app = Dash(external_stylesheets=[dbc.themes.LUMEN, dbc.icons.FONT_AWESOME])

# cache = diskcache.Cache("./cache")
# long_callback_manager = DiskcacheLongCallbackManager(cache)
# mapbox_token = " "

app.layout = [
    html.Div(
        children=[
            html.Div(
                children=[
                    html.H1(
                        children=[
                            html.I(className="fa-solid fa-graduation-cap"),
                            "ตรวจสอบจำนวนการรับนักศึกษา ของมหาวิทยาลัย คณะ ที่ต้องการผ่านการเลือก",
                        ],
                        style={
                            "width": "100%",
                            "display": "flex",
                            "padding": "1rem",
                            "padding-left": "3rem",
                            "box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.5)",
                            "font-weight": "600",
                            "gap": "10px",
                        },
                    )
                ]
            ),
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.H1(children=["ผลการเลือกตามสายที่ชื่นชอบ"]),
                            dcc.Graph(
                                id="graph-1",
                                style={
                                    "position": "relative",
                                    "zIndex": "100",
                                },
                            ),
                        ]
                    ),
                    html.Div(
                        children=[
                            html.Div(
                                children=[
                                    html.I(className="fa-regular fa-thumbs-up"),
                                    "เลือกตามสายที่ชื่นชอบ",
                                ],
                                style=styles.header_secrch,
                            ),
                            html.Div(
                                children=[
                                    html.Div(
                                        children=[
                                            html.Div(
                                                children=["มหาวิทยาลัย"],
                                            ),
                                            dcc.Dropdown(
                                                options=df["university"].unique(),
                                                clearable=True,
                                                searchable=True,
                                                id="university-dd",
                                                style={
                                                    "position": "relative",
                                                    "zIndex": "999",
                                                },
                                            ),
                                        ]
                                    ),
                                    html.Div(
                                        children=[
                                            html.Div(
                                                children=["คณะ"],
                                            ),
                                            dcc.Dropdown(
                                                options=df["major"].unique(),
                                                clearable=True,
                                                searchable=True,
                                                id="major-dd",
                                                style={
                                                    "position": "relative",
                                                    "zIndex": "999",
                                                },
                                            ),
                                        ]
                                    ),
                                    html.Div(
                                        children=[
                                            html.Div(
                                                children=["หลักสูตร"],
                                            ),
                                            dcc.Dropdown(
                                                options=df["course"].unique(),
                                                clearable=True,
                                                searchable=True,
                                                id="course-dd",
                                                style={
                                                    "position": "relative",
                                                    "zIndex": "998",
                                                },
                                            ),
                                        ]
                                    ),
                                ],
                                style=styles.grid_container,
                            ),
                        ],
                        style=styles.bg_search,
                    ),
                    html.Div(
                        children=[
                            html.H1(
                                children=["ผลการเลือกตามประเภทหลักสูตร"],
                                style={
                                    "border-top": "3px solid orange",
                                    "padding-top": "3rem",
                                    "margin-top": "4rem",
                                },
                            ),
                            dcc.Graph(
                                id="graph-2",
                                style={
                                    "position": "relative",
                                    "zIndex": "100",
                                },
                            ),
                        ]
                    ),
                    html.Div(
                        children=[
                            html.Div(
                                children=[
                                    html.I(className="fa-solid fa-book"),
                                    "เลือกตามประเภทหลักสูตร",
                                ],
                                style=styles.header_secrch,
                            ),
                            html.Div(
                                children=[
                                    html.Div(
                                        children=[
                                            html.Div(
                                                id="slider-output-container",
                                            ),
                                            dcc.RangeSlider(
                                                min=2000,
                                                max=130000,
                                                id="my-slider",
                                                value=[12000, 20000],
                                            ),
                                        ],
                                        style={
                                            "display": "grid",
                                            "grid-template-columns": "main right right right right",
                                            "padding": "10px",
                                        },
                                    ),
                                    html.Div(
                                        children=[
                                            html.Div(
                                                children=["ประเภทหลักสูตร"],
                                            ),
                                            dcc.Dropdown(
                                                options=df["ประเภทหลักสูตร"].unique(),
                                                clearable=True,
                                                searchable=True,
                                                id="degree-dd",
                                                style={
                                                    "position": "relative",
                                                    "zIndex": "998",
                                                },
                                            ),
                                        ]
                                    ),
                                    html.Div(
                                        children=[
                                            html.Div(
                                                children=["มหาวิทยาลัย"],
                                            ),
                                            dcc.Dropdown(
                                                options=df["university"].unique(),
                                                clearable=True,
                                                searchable=True,
                                                id="university-dd2",
                                                style={
                                                    "position": "relative",
                                                    "zIndex": "999",
                                                },
                                            ),
                                        ]
                                    ),
                                ],
                                style=styles.grid_container,
                            ),
                        ],
                        style=styles.bg_search,
                    ),
                ],
                style={"margin": "2rem"},
            ),
        ],
        style={
            "background": "rgb(255,248,238)",
            "height": "100%",
            "padding-bottom": "10rem",
        },
    )
]


@callback(Output("slider-output-container", "children"), Input("my-slider", "value"))
def update_slider_output(value):
    return "ค่าเทอมต่ำกว่า : {}".format(value if value else "-")


@callback(Output("major-dd", "options"), Input("university-dd", "value"))
def update_major_options(value):
    if value:
        return df[df["university"] == value]["major"].unique()
    return df["major"].unique()


@callback(
    Output("course-dd", "options"),
    Input("university-dd", "value"),
    Input("major-dd", "value"),
)
def update_course_options(university, major):
    if university and not major:
        return df[df["university"] == university]["course"].unique()
    elif not university and major:
        return df[df["major"] == major]["course"].unique()
    elif university and major:
        df1 = df[df["university"] == university]
        return df1[df1["major"] == major]["course"].unique()
    return df["course"].unique()


@callback(
    Output("graph-1", "figure"),
    Input("university-dd", "value"),
    Input("major-dd", "value"),
    Input("course-dd", "value"),
)
def update_bar_graph(university, major, course, df=df):
    # fig = None
    if not university and not major and not course:
        university = "จุฬาลงกรณ์มหาวิทยาลัย"
    if (university and major and course) or (university and course):
        df = df[df["university"] == university]
        if major:
            df = df[df["major"] == major]
        df = df[df["course"] == course]
        try:
            data = {
                "round": [
                    "รอบ 1 Portfolio",
                    "รอบ 2 Quota",
                    "รอบ 3 Admission",
                    "รอบ 4 Direct Admission",
                ],
                "value": [
                    df["รอบ 1 Portfolio"].to_list()[0],
                    df["รอบ 2 Quota"].to_list()[0],
                    df["รอบ 3 Admission"].to_list()[0],
                    df["รอบ 4 Direct Admission"].to_list()[0],
                ],
                "cost": [str(df["ค่าใช้จ่าย"].to_list()[0]) for i in range(4)],
                "ชื่อหลักสูตรภาษาอังกฤษ": [
                    df["ชื่อหลักสูตรภาษาอังกฤษ"].to_list()[0] for i in range(4)
                ],
            }
        except:
            data = {
                "round": [
                    "รอบ 1 Portfolio",
                    "รอบ 2 Quota",
                    "รอบ 3 Admission",
                    "รอบ 4 Direct Admission",
                ],
                "value": [0, 0, 0, 0],
                "cost": [0, 0, 0, 0],
                "ชื่อหลักสูตรภาษาอังกฤษ": ["-", "-", "-", "-"],
            }
        fig = px.pie(
            data,
            values="value",
            names="round",
            labels={
                "round": "รอบ TCAS",
                "major": "คณะ",
                "value": "จำนวนที่รับ",
            },
            hover_name="round",
            hover_data=["cost"],
            title="กราฟวงกลมแสดงข้อมูลจำนวนการรับนักศึกษาจากมหาวิทยาลัย {}{}หลักสูตร{}".format(
                university, (" คณะ" + major + " ") if major else "", course
            ),
        )
    else:
        if university:
            df = df[df["university"] == university]
        if major:
            df = df[df["major"] == major]
        if course:
            df = df[df["course"] == course]
        fig = px.bar(
            df,
            x="major",
            y=[
                "รอบ 1 Portfolio",
                "รอบ 2 Quota",
                "รอบ 3 Admission",
                "รอบ 4 Direct Admission",
            ],
            title=f"กราฟแสดงข้อมูลจำนวนการรับนักศึกษาจากมหาวิทยาลัย {university}",
            barmode="group",
            text="value",
            labels={
                "variable": "รอบ TCAS",
                "major": "คณะ",
                "university": "มหาวิทยาลัย",
            },
            hover_name="ชื่อหลักสูตร",
            hover_data=[
                "university",
                "ชื่อหลักสูตรภาษาอังกฤษ",
                "ประเภทหลักสูตร",
                "วิทยาเขต",
                "ค่าใช้จ่าย",
                "ชื่อหลักสูตร",
            ],
        )
        if university:
            fig.update_traces(
                textposition="outside",
            )

    fig.update_layout(
        paper_bgcolor="rgba(255,255,255,0.5)",
    )
    return fig


@callback(
    Output("graph-2", "figure"),
    Input("degree-dd", "value"),
    Input("my-slider", "value"),
    Input("university-dd2", "value"),
)
def update_bar_graph_2(degree, slider, university, df=df):
    if degree:
        df = df[df["ประเภทหลักสูตร"] == degree]

    if university:
        df = df[df["university"] == university]

    if slider:
        df = df[df["ค่าใช้จ่าย"] >= slider[0]]
        df = df[df["ค่าใช้จ่าย"] <= slider[1]]
    df = df.sort_values(["ค่าใช้จ่าย", "university", "major", "ประเภทหลักสูตร"])
    fig1 = px.bar(
        df,
        x="major",
        y=[
            "รอบ 1 Portfolio",
            "รอบ 2 Quota",
            "รอบ 3 Admission",
            "รอบ 4 Direct Admission",
        ],
        title=f"กราฟแสดงข้อมูลจำนวนการรับนักศึกษาจากมหาวิทยาลัยตามเงื่อนไขที่กำหนด",
        text="value",
        labels={
            "variable": "รอบ TCAS",
            "major": "คณะ",
            "university": "มหาวิทยาลัย",
        },
        hover_name="ชื่อหลักสูตร",
        hover_data=[
            "ชื่อหลักสูตรภาษาอังกฤษ",
            "ประเภทหลักสูตร",
            "วิทยาเขต",
            "ค่าใช้จ่าย",
            "ชื่อหลักสูตร",
            "university",
        ],
    )
    fig1.update_layout(
        paper_bgcolor="rgba(255,255,255,0.5)",
    )
    return fig1


if __name__ == "__main__":
    app.run(debug=True)
