from dataclasses import dataclass
from bakery import assert_equal
from drafter import *

set_website_title("Bird Identifier")
set_site_information(
    author="Ashleigh Cheeseman",
    description="Use specific characteristics to identify a bird.",
    sources="Drafter Docs",
    planning=["Copy of CS1 Final Project 0_ Pick a Problem.pdf","CS1 Final Project 1_ Design.pdf"],
    links=["https://github.com/ashleighcheeseman/bird-identifier"]
)

hide_debug_information()
set_website_framed(False)

@dataclass
class Bird:
    name: str
    main_colors: list[str]
    habitat: list[str]
    size: str
    
@dataclass
class State:
    selected_colors: list[str]
    selected_habitats:list[str]
    selected_size:str
    matching_birds: list[Bird]
    
BIRDS = [
    Bird("American Robin", ["Orange", "Brown", "Gray"],
         ["Forests", "Woodlands", "Urban", "Fields"], "Medium"),
    Bird("Northern Cardinal", ["Red", "Black"],
         ["Woodlands", "forests", "Urban"], "Medium"),
    Bird("Blue Jay", ["Blue", "White", "Black"],
         ["Forests", "Woodlands", "Urban"], "Medium"),
    Bird("American Goldfinch", ["Yellow", "Black", "White"],
         ["Fields", "Grasslands", "Urban"], "Small"),
    Bird("House Sparrow", ["Brown", "Gray", "Black"],
         ["Urban", "Fields", "Grasslands"], "Small"),
    Bird("Mourning Dove", ["Gray", "Brown"],
         ["Woodlands", "Fields", "Urban", "Grasslands"], "Medium"),
    Bird("Downy Woodpecker", ["Black", "White", "Red"],
         ["Forests", "Woodlands", "Urban"], "Small"),
    Bird("Red-bellied Woodpecker", ["Red", "Black", "White", "Gray"],
         ["Forests", "Woodlands", "Urban"], "Medium"),
    Bird("Black-capped Chickadee", ["Black", "White", "Gray"],
         ["Forests", "Woodlands"], "Small"),
    Bird("Tufted Titmouse", ["Gray", "White", "Brown"],
         ["Forests", "Woodlands", "Urban"], "Small"),
    Bird("Eastern Bluebird", ["Blue", "Orange", "White"],
         ["Fields", "Grasslands", "Woodlands"], "Small"),
    Bird("House Finch", ["Red", "Brown", "Gray"],
         ["Urban", "Fields", "Woodlands"], "Small"),
    Bird("Common Grackle", ["Black", "Blue", "Green"],
         ["Wetlands", "Fields", "Urban", "Grasslands"], "Medium"),
    Bird("Mallard", ["Green", "Brown", "White", "Gray"],
         ["Wetlands", "Fields", "Urban"], "Large"),
    Bird("Canada Goose", ["Brown", "Black", "White"],
         ["Wetlands", "Fields", "Grasslands", "Urban"], "Large"),
    Bird("Great Blue Heron", ["Blue", "Gray", "White"],
         ["Wetlands", "Fields"], "Large"),
    Bird("Red-tailed Hawk", ["Brown", "White", "Red"],
         ["Forests", "Grasslands", "Fields", "Woodlands"], "Large"),
    Bird("Bald Eagle", ["Brown", "White", "Yellow"],
         ["Forests", "Wetlands"], "Large"),
    Bird("Wild Turkey", ["Brown", "Black", "Gray"],
         ["Woodlands", "Forests", "Fields"], "Large"),
    Bird("Barn Swallow", ["Blue", "Orange", "White"],
         ["Fields", "Grasslands", "Wetlands", "Urban"], "Small")
]
    

    
@route
def index(state:State)->Page:
    """
    returns home page of website, has button to lead to search
    """
    return Page(state, [
        Header("Bird Search Engine",1),
        Text("Welcome, Use this search engine to identify a bird!"),
        Text("You can search using the bird's main colors, habitat, and size."),
        Button("Start Searching", "select_colors")
        ])

@route
def select_colors(state:State)->Page:
    """
    returns a page with color options, uses RelatedCheckBox so the user can
    select multiple colors and they are stored in a list
    """
    return Page(state, [
        Header("What colors were the bird?",2),
        Text("Select all the colors you noticed."),
        RelatedCheckBox("colors", "Blue"),
        " Blue",
        RelatedCheckBox("colors", "Red"),
        " Red",
        RelatedCheckBox("colors", "Yellow"),
        " Yellow",
        RelatedCheckBox("colors", "Green"),
        " Green",
        RelatedCheckBox("colors", "Orange"),
        " Orange",
        RelatedCheckBox("colors", "Black"),
        " Black",
        RelatedCheckBox("colors", "White"),
        " White",
        RelatedCheckBox("colors", "Brown"),
        " Brown",
        RelatedCheckBox("colors", "Gray"),
        " Gray",
        Button("Continue","select_habitat")
    ])
    
    
@route
def select_habitat(state:State)->Page:
    """
    user selects from options for habitats, again uses RelatedCheckBox
    """
    return Page(state, [
        Header("What habitat was the bird in?",2),
        Text("Select the habitat"),
        RelatedCheckBox("habitats","Forests"),
        " Forest",
        RelatedCheckBox("habitats","Woodlands"),
        " Woodlands",
        RelatedCheckBox("habitats","Wetlands"),
        " Wetlands",
        RelatedCheckBox("habitats","Fields"),
        " Fields",
        RelatedCheckBox("habitats","Grasslands"),
        " Grasslands",
        RelatedCheckBox("habitats","Urban"),
        " Urban",
        Button("Continue","select_size")
    ])


@route
def select_size(state:State)->Page:
    """
    gives three options of size, the user only picks one
    """
    return Page(state,[
        Header("What size was the bird?",2),
        Text("Select from these sizes"),
        SelectBox("size",["Small","Medium","Large"]),
        Button("Continue", "/search_results")
    ])

state3 = State(["Blue"], ["Forests"], "", BIRDS)

result3 = select_size(state3)

assert_equal(state3.selected_colors, ["Blue"])
assert_equal(state3.selected_habitats, ["Forests"])
assert_equal(state3.selected_size, "")

@route
def after_colors(state: State, colors: list[str]) -> Page:
    """
    saves the colors and changes the state
    """
    state.selected_colors = colors
    return select_habitat(state)

state1 = State([], [], "", BIRDS)

result1 = after_colors(state1, ["Blue", "White"])

assert_equal(state1.selected_colors, ["Blue", "White"])

@route
def after_habitat(state: State, habitats: list[str]) -> Page:
    """
    saves the habitats and changes the state
    """
    state.selected_habitats = habitats
    return select_size(state)

state2 = State(["Blue"], [], "", BIRDS)

result2 = after_habitat(state2, ["Forests", "Wetlands"])

assert_equal(state2.selected_habitats, ["Forests", "Wetlands"])


@route
def search_results(state: State, size: str) -> Page:
    """
    uses user inputs and keeps score of which birds best match the inputs
    uses join to turn a list of strings into a single string with ", " separating
    uses break to end a loop after one instance is found
    """
    state.selected_size = size
    
    if (state.selected_colors == [] and
    state.selected_habitats == [] and
    size == ""):
        state.matching_birds = BIRDS

    else:
        
        bird_scores = []

        highest_score = -1

        for bird in BIRDS:
            score = 0

            for color in state.selected_colors:
                if color in bird.main_colors:
                    score = 1
                    break

            for habitat in state.selected_habitats:
                if habitat in bird.habitat:
                    score += 1
                    break

            if state.selected_size == bird.size:
                score += 1

            bird_scores.append((bird, score))

            if score > highest_score:
                highest_score = score

        state.matching_birds = []

        if highest_score > 0:
            for bird, score in bird_scores:
                if score == highest_score:
                    state.matching_birds.append(bird)

    content = [
        Header("Your Bird Search Results", 1),
        Text("Here are the birds that best match your selections:")
    ]

    if state.matching_birds == []:
         content.append(Text("Sorry! No birds were found."))
    else:
        for bird in state.matching_birds:
            content.append(Header(bird.name, 2))
            content.append(Text("Colors: " + ", ".join(bird.main_colors)))
            content.append(Text("Habitats: " + ", ".join(bird.habitat)))
            content.append(Text("Size: " + bird.size))

    content.append(Button("Refine Search", "/refine_search"))
    content.append(Button("Start Over", "/return_to_start"))

    return Page(state, content)

state4 = State([], [], "", BIRDS)

result4 = search_results(state4, "")

assert_equal(state4.selected_size, "")
assert_equal(state4.matching_birds, BIRDS)

state5 = State(
    [BIRDS[0].main_colors[0]],
    [BIRDS[0].habitat[0]],
    "",
    BIRDS
)

result5 = search_results(state5, BIRDS[0].size)

assert_equal(state5.selected_size, BIRDS[0].size)

assert_equal(BIRDS[0] in state5.matching_birds, True)

state6 = State(["Purple"], ["Desert"], "", BIRDS)

result6 = search_results(state6, "Extra Large")

assert_equal(state6.matching_birds, [])

@route
def refine_search(state:State)->Page:
    """
    returns a page of buttons that lead back to other pages to change selections
    also has option to reset
    """
    return Page(state, [
        Header("Refine your search.",1),
        Text("What would you like to change?"),
        Button("Change colors", "/select_colors"),
        Button("Change habitats", "select_habitat"),
        Button("Change size", "/select_size"),
        Button("View Current Results", "/view_current_results"),
        Button("Start Over", "/return_to_start")
    ])

state7 = State(
    ["Blue", "White"],
    ["Forests"],
    "Medium",
    BIRDS
)

result7 = refine_search(state7)

assert_equal(state7.selected_colors, ["Blue", "White"])
assert_equal(state7.selected_habitats, ["Forests"])
assert_equal(state7.selected_size, "Medium")

@route
def view_current_results(state: State) -> Page:
    """
    displays the current results and the current selections
    """
    content = [
        Header("Your Bird Search Results", 1),
        Text("Here are your current matching birds:")
    ]

    if state.matching_birds == []:
        content.append(Text("No birds matched your selections."))
    else:
        for bird in state.matching_birds:
            content.append(Header(bird.name, 2))
            content.append(Text("Colors: " + ", ".join(bird.main_colors)))
            content.append(Text("Habitats: " + ", ".join(bird.habitat)))
            content.append(Text("Size: " + bird.size))

    content.append(Button("Refine Search", "/refine_search"))
    content.append(Button("Start Over", "/return_to_start"))

    return Page(state, content)

state8 = State(
    ["Blue"],
    ["Forests"],
    "Medium",
    [BIRDS[0], BIRDS[1]]
)

result8 = view_current_results(state8)

assert_equal(state8.matching_birds, [BIRDS[0], BIRDS[1]])
assert_equal(state8.selected_colors, ["Blue"])
assert_equal(state8.selected_habitats, ["Forests"])
assert_equal(state8.selected_size, "Medium")
state9 = State([], [], "", [])

result9 = view_current_results(state9)

assert_equal(state9.matching_birds, [])

@route
def return_to_start(state:State)-> Page:
    """
    returns state to empty/original and returns start page
    """
    state.selected_colors=[]
    state.selected_habitats=[]
    state.selected_size=""
    state.matching_birds= BIRDS
    return index(state)

state10 = State(
    ["Blue", "White"],
    ["Forests", "Wetlands"],
    "Large",
    [BIRDS[0]]
)

result10 = return_to_start(state10)

assert_equal(state10.selected_colors, [])
assert_equal(state10.selected_habitats, [])
assert_equal(state10.selected_size, "")
assert_equal(state10.matching_birds, BIRDS)

start_server(State(
    selected_colors=[],
    selected_habitats=[],
    selected_size="",
    matching_birds=BIRDS
))
