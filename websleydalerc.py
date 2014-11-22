from websleydale import build, copy, directory, menu, pandoc, set_defaults
from websleydale.sources import Dir, Git

local = Dir(".")
pages = Dir("pd")
htaccess = Dir("htaccess")
recipes = Git("https://github.com/kalgynirae/recipes.git")
rockuefort = Git("https://github.com/kalgynirae/rockuefort.git")
routemaster = Git("https://github.com/routemaster/routemaster-frontend.git")
subjunctive = Git("https://github.com/kalgynirae/subjunctive.git")
think_green = Git("https://github.com/kalgynirae/thinking-green.git")
websleydale_ = Git("https://github.com/kalgynirae/websleydale.git",
                   checkout='test')

root = directory({
    ".htaccess": htaccess["root"],
    "files/.htaccess": htaccess["files"],
    "files/public/.htaccess": htaccess["files_public"],

    "css": local["css"],
    "font": local["font"],
    "image": local["image"],
    "media": local["media"],
    "favicon.ico": local["image/favicon.ico"],

    "robots.txt": pages["robots.txt"],
    "404.shtml": pandoc(pages["404.pd"]),
    "index.html": pandoc(pages["index.pd"]),
    "music.html": pandoc(pages["music.pd"]),
    "boxer.html": pandoc(pages["boxer.pd"]),
    "jabberwockus.html": pandoc(pages["jabberwockus.pd"]),
    "krypto.html": pandoc(pages["krypto.pd"], header=pages["krypto.header"]),
    "cafe": directory({
        "index.html": pandoc(pages["cafe/index.pd"]),
    }),
    "colin/index.html": pandoc(pages["colin/index.pd"]),
    "colin/events.html": pandoc(pages["colin/events.pd"]),
    "recipes": directory({
        "%s.html" % name: pandoc(recipes["%s.pd" % name]) for name in [
            "almond_salad_dressing",
            "banana_bread",
            "beef_curry",
            "chili",
            "christmas_anything",
            "cookies",
            "creme_brulee_cheesecake",
            "mung_bean_dal",
            "pumpkin_bread",
            "quiche",
            "sugar_cookies",
            "sweet_potato_casserole",
            "thai_chicken_curry",
        ]
    }),
    "projects": directory({
        "rockuefort/index.html": pandoc(rockuefort["README.md"]),
        "routemaster/index.html": pandoc(routemaster["README.md"], toc=True),
        "subjunctive/index.html": pandoc(subjunctive["README.md"]),
        "think-green/index.html": pandoc(think_green["README.md"]),
        "websleydale/index.html": pandoc(websleydale_["README.md"]),
    }),
    "tools": directory({
        "stopwatch.html": pandoc(pages["tools/stopwatch.pd"], header=pages["tools/stopwatch.header"]),
    }),
    "wiki": directory({
        "%s.html" % name: pandoc(pages["wiki/%s.pd" % name]) for name in [
            "dragee",
            "early-twenty-first-century",
            "the-caring-continuum",
            "games/capture-the-flag",
            "games/narchanso",
            "games/the-base-game",
            "games/trebuchennis",
        ]
    }),
})

menu_ = menu([
    ("index", "/"),
    ("music", "/music.html"),
    ("projects", "/projects/"),
    ("recipes", "/recipes/"),
    ("tools", "/tools/"),
    ("wiki", "/wiki/"),
    ("café", "/cafe/"),
])

#redirects = {
#    "/games/narchanso.html": "/wiki/narchanso-ball.html",
#    "/recipes/mung_bean_dahl.html": "/recipes/mung_bean_dal.html",
#}

set_defaults(
    menu=menu_,
    template=local["templates/lumeh.html"],
)

build("out", root)
