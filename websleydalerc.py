from websleydale import build, copy, directory, menu, pandoc, set_defaults
from websleydale.sources import Dir, Git

local = Dir(".")
pages = Dir("md")
htaccess = Dir("htaccess")
pchyme = Git("https://github.com/kalgynirae/pchyme.git")
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
    "docs": local["docs"],
    "font": local["font"],
    "guess": local["guess"],
    "image": local["image"],
    "js": local["js"],
    "media": local["media"],
    "favicon.ico": local["image/favicon.ico"],
    "japanese_names.py": local["japanese_names.py"],

    "robots.txt": pages["robots.txt"],
    "index.html": pandoc(pages["index.md"]),
    "music.html": pandoc(pages["music.md"]),
    "boxer.html": pandoc(pages["boxer.md"]),
    "jabberwockus.html": pandoc(pages["jabberwockus.md"]),
    "lumeh.html": pandoc(pages["lumeh.md"]),
    "poetry-yay.html": pandoc(pages["poetry-yay.md"]),
    "krypto.html": pandoc(pages["krypto.md"], header=pages["krypto.header"]),
    "cafe": directory({
        "index.html": pandoc(pages["cafe/index.md"]),
    }),
    "colin/index.html": pandoc(pages["colin/index.md"]),
    "error": directory({
        "%s.html" % name: pandoc(pages["error/%s.md" % name]) for name in [
            "404",
        ]
    }),
    "recipes": directory(dirlist="Recipes", tree={
        "%s.html" % name: pandoc(recipes["%s.md" % name]) for name in [
            "almond_salad_dressing",
            "asparagus_mushroom_soup",
            "banana_bread",
            "beef_curry",
            "bettys_chili",
            "calico_beans",
            "chana_masala",
            "chana_masala_with_spice_kit",
            "chancakes",
            "chicken_curry",
            "chili",
            "christmas_anything",
            "cookies",
            "creme_brulee_cheesecake",
            "green_bean_bundles",
            "mac_and_cheese",
            "monday_krishna_dal",
            "mung_bean_dal",
            "pumpkin_bread",
            "quiche",
            "spinach",
            "sugar_cookies",
            "sweet_potato_casserole",
            "thai_chicken_curry",
            "tuesday_krishna",
        ]
    }),
    "projects": directory(dirlist="Projects", tree={
        "pchyme/index.html": pandoc(pchyme["README.md"]),
        "rockuefort/index.html": pandoc(rockuefort["README.md"]),
        "routemaster/index.html": pandoc(routemaster["README.md"], toc=True),
        "subjunctive/index.html": pandoc(subjunctive["README.md"]),
        "think-green/index.html": pandoc(think_green["README.md"]),
        "websleydale/index.html": pandoc(websleydale_["README.md"]),
    }),
    "tools": directory(dirlist="Tools", tree={
        "stopwatch.html": pandoc(pages["tools/stopwatch.md"], header=pages["tools/stopwatch.header"]),
    }),
    "wiki": directory(dirlist="Wiki", tree={
        "%s.html" % name: pandoc(pages["wiki/%s.md" % name]) for name in [
            "dragee",
            "early-twenty-first-century",
            "the-caring-continuum",
            "thestruggle",
            "games/capture-the-flag",
            "games/narchanso",
            "games/the-base-game",
            "games/trebuchennis",
        ]
    }),
})

menu_ = menu([
    ("index", "/"),
    ("blog", "http://blog.lumeh.org/"),
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
    header_template=local["templates/header.html"],
    footer_template=local["templates/footer.html"],
)

build("out", root)
