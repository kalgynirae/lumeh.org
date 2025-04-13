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
    root,
    sass,
)


def page(source):
    return jinja(markdown(source), template="page.html")


site = Site(
    known_authors={
        Author(
            display_name="Colin",
            emails={"colinchan@lumeh.org", "colin+git@lumeh.org"},
            url="https://github.com/kalgynirae",
        ),
        Author(
            display_name="tylerlaprade",
            emails={"pinkmonkeyblue@gmail.com"},
            url="https://github.com/tylerlaprade",
        ),
    },
    name="lumeh.org",
    repo_name="kalgynirae/lumeh.org",
    repo_url="https://github.com/kalgynirae/lumeh.org",
    tree={
        "assets": dir(root / "assets"),
        "css/lumeh.css": sass(root / "css/lumeh.sass"),
        "docs": dir(root / "docs"),
        "font": dir(root / "font"),
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
            f"projects/{path.name}/": page(path / "README.md")
            for path in root.glob("projects/*")
            if not path.name == "recipes"
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
build(site, dest="out")
