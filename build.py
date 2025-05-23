import logging
from collections import ChainMap
from functools import partial

from websleydale import (
    Author,
    Site,
    build,
    dir,
    fake,
    file,
    index,
    jinja,
    markdown,
    merge,
    root,
    sass,
)


def page(source, *, title: str | None = None):
    return jinja(markdown(source), template="page.html", title=title)


site = Site(
    known_authors={
        Author(
            display_name="Colin",
            emails={"colinchan@lumeh.org", "colin+git@lumeh.org"},
            url="https://github.com/kalgynirae",
        ),
        Author(
            display_name="Benjamin",
            emails={"github@benjam.info"},
            url="https://github.com/bgw",
        ),
        Author(
            display_name="Tyler",
            emails={"pinkmonkeyblue@gmail.com"},
            url="https://github.com/tylerlaprade",
        ),
    },
    name="lumeh.org",
    repo_name="kalgynirae/lumeh.org",
    repo_url="https://github.com/kalgynirae/lumeh.org",
    tree={
        "css/lumeh.css": sass(root / "css/lumeh.sass"),
        "docs": dir(root / "docs"),
        "files": dir(root / "assets/files"),
        "font": merge(dir(root / "font"), dir(root / "assets/font")),
        "guess": dir(root / "guess"),
        "image": dir(root / "image"),
        "js": dir(root / "js"),
        "media": dir(root / "media"),
        "redirects.conf": file(root / "redirects.conf"),
        "redirects.caddy": file(root / "redirects.caddy"),
        "robots.txt": file(root / "robots.txt"),
        **index({
            (
                f"{path.relative_to(root/'pages').with_suffix('.html')}"
                if path.name == "index.md"
                else f"{path.relative_to(root/'pages').with_suffix('')}/"
            ): page(path)
            for path in root.glob("pages/**/*.md")
        }, "poetry", "tools"),
        **index({
            "projects/lumeh.org/": page(root / "README.md", title="lumeh.org"),
            "projects/pchyme/": page(root / "projects/pchyme/README.md", title="pchyme"),
            "projects/rockuefort/": page(root / "projects/rockuefort/README.md", title="Rockuefort"),
            "projects/sfago2024.org/": page(root / "projects/sfago2024.org.md", title="sfago2024.org"),
            "projects/slideception/": page(root / "projects/slideception/README.md", title="slideception"),
            "projects/thinking-green/": page(root / "projects/thinking-green/README.md", title="Thinking Green"),
            "projects/voidpop/": page(root / "projects/voidpop/README.md", title="Voidpop"),
            "projects/websleydale/": page(root / "projects/websleydale/README.md", title="Websleydale"),
        }, "projects"),
        **index({
            f"recipes/{name.replace('_', '-')}/": page(
                root / f"projects/recipes/{name}.md"
            )
            for name in [
                "almond_salad_dressing",
                "apple_cider",
                "apple_crisp",
                "asparagus_mushroom_soup",
                "banana_bread",
                "bettys_chili",
                "calico_beans",
                "chana_masala",
                "chana_masala_with_spice_kit",
                "chancakes",
                "chicken_curry",
                "chicken_curry_v2",
                "chickpeas_pressure_cooker",
                "chili",
                "chonklate_chip_cookies",
                "christmas_anything",
                "cookies",
                "cottage_pie",
                "creme_brulee_cheesecake",
                "curry_chicken_pot_pie",
                "dal",
                "first_watch_seasoning",
                "green_bean_bundles",
                "krishna_lunch_chili",
                "lemonade",
                "little_white_ball_cookies",
                "mac_and_cheese",
                "popovers",
                "pumpkin_bread",
                "quiche",
                "salmon_pate",
                "shortbread_cookies",
                "sweet_potato_casserole",
                "thai_chicken_curry",
            ]
        }, "recipes"),
    },
)

logging.basicConfig(level=logging.INFO, format="%(message)s")
build(site, dest="out")
