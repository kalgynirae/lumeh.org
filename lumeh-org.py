import logging

from websleydale import (
    Author,
    Redirect,
    build,
    caddy_redirects,
    dir,
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


logging.basicConfig(level=logging.INFO, format="%(message)s")

perm = Redirect.permanent
temp = Redirect.temporary

redirects = {
    "/andersonorgan": perm(
        "/media/theandrewandersonmemorialpipeorganahistory-wittine.pdf"
    ),
    "/boxer.html": perm("/boxer/"),
    "/cookies": temp("/projects/lumeh.org/#cookies"),
    "/cookies/": temp("/projects/lumeh.org/#cookies"),
    "/docs/resume-20200720.pdf": perm("/files/resume-20200720.pdf"),
    "/docs/resume-20241215.pdf": perm("/files/resume-20241215.pdf"),
    "/games/narchanso.html": perm("/wiki/games/narchanso-ball/"),
    "/jabberwockus.html": perm("/poetry/jabberwockus/"),
    "/krypto.html": perm("/tools/krypto-generator/"),
    "/lumeh.html": perm("/poetry/lumeh-god-of-light-bulbs/"),
    "/music.html": perm("/music/"),
    "/papenago-just-add-feet-2025": perm(
        "https://docs.google.com/forms/d/e/1FAIpQLSdFVPWN3D_JJyHh1rnq00w0MpdP2FpN_ZpGveb1cCivSN5poQ/viewform?usp=sharing"
    ),
    "/poetry-yay.html": perm("/poetry/poetry-yay/"),
    "/recipes/almond_salad_dressing.html": perm("/recipes/almond-salad-dressing/"),
    "/recipes/apple_cider.html": perm("/recipes/apple-cider/"),
    "/recipes/apple_crisp.html": perm("/recipes/apple-crisp/"),
    "/recipes/asparagus_mushroom_soup.html": perm("/recipes/asparagus-mushroom-soup/"),
    "/recipes/banana_bread.html": perm("/recipes/banana-bread/"),
    "/recipes/bettys_chili.html": perm("/recipes/bettys-chili/"),
    "/recipes/calico_beans.html": perm("/recipes/calico-beans/"),
    "/recipes/chana_masala.html": perm("/recipes/chana-masala/"),
    "/recipes/chana_masala_with_spice_kit.html": perm(
        "/recipes/chana-masala-with-spice-kit/"
    ),
    "/recipes/chancakes.html": perm("/recipes/chancakes/"),
    "/recipes/chicken_curry.html": perm("/recipes/chicken-curry/"),
    "/recipes/chili.html": perm("/recipes/chili/"),
    "/recipes/christmas_anything.html": perm("/recipes/christmas-anything/"),
    "/recipes/cookies.html": perm("/recipes/cookies/"),
    "/recipes/cottage_pie.html": perm("/recipes/cottage-pie/"),
    "/recipes/creme_brulee_cheesecake.html": perm("/recipes/creme-brulee-cheesecake/"),
    "/recipes/dal.html": perm("/recipes/dal/"),
    "/recipes/first_watch_seasoning.html": perm("/recipes/first-watch-seasoning/"),
    "/recipes/green_bean_bundles.html": perm("/recipes/green-bean-bundles/"),
    "/recipes/mac_and_cheese.html": perm("/recipes/mac-and-cheese/"),
    "/recipes/mung_bean_dahl.html": perm("/recipes/dal/"),
    "/recipes/popovers.html": perm("/recipes/popovers/"),
    "/recipes/pumpkin_bread.html": perm("/recipes/pumpkin-bread/"),
    "/recipes/quiche.html": perm("/recipes/quiche/"),
    "/recipes/sweet_potato_casserole.html": perm("/recipes/sweet-potato-casserole/"),
    "/recipes/thai_chicken_curry.html": perm("/recipes/thai-chicken-curry/"),
    "/report-a-problem": temp("/projects/lumeh.org/#reporting-problems"),
    "/report-a-problem/": temp("/projects/lumeh.org/#reporting-problems"),
    "/tools/stopwatch.html": perm("/tools/stopwatch/"),
    "/wiki/dragee.html": perm("/wiki/dragee/"),
    "/wiki/early-twenty-first-century.html": perm("/wiki/early-twenty-first-century/"),
    "/wiki/games/capture-the-flag.html": perm("/wiki/games/capture-the-flag/"),
    "/wiki/games/narchanso-ball.html": perm("/wiki/games/narchanso-ball/"),
    "/wiki/games/the-base-game.html": perm("/wiki/games/the-base-game/"),
    "/wiki/games/trebuchennis.html": perm("/wiki/games/trebuchennis/"),
    "/wiki/linux/colorize": perm("/projects/colorby/"),
    "/wiki/linux/colorize/": perm("/projects/colorby/"),
    "/wiki/opposites.html": perm("/wiki/opposites/"),
    "/wiki/the-caring-continuum.html": perm("/wiki/the-caring-continuum/"),
    "/wiki/thestruggle.html": perm("/wiki/thestruggle/"),
}

build(
    dest="out",
    known_authors={
        Author(
            display_name="Colin",
            full_name="Colin Chan",
            emails={"colinchan@lumeh.org", "colin+git@lumeh.org"},
            url="https://github.com/kalgynirae",
        ),
        Author(
            display_name="Benjamin",
            full_name="Benjamin Woodruff",
            emails={"github@benjam.info"},
            url="https://github.com/bgw",
        ),
        Author(
            display_name="Tyler",
            full_name="Tyler Laprade",
            emails={"pinkmonkeyblue@gmail.com"},
            url="https://github.com/tylerlaprade",
        ),
    },
    name="lumeh.org",
    repo_name="kalgynirae/lumeh.org",
    repo_url="https://github.com/kalgynirae/lumeh.org",
    tree={
        "css/lumeh.css": sass(root / "css/lumeh.sass"),
        "files": dir(root / "assets/files", allow_missing=True),
        "font": merge(
            dir(root / "font"), dir(root / "assets/font", allow_missing=True)
        ),
        "guess": dir(root / "guess"),
        "image": dir(root / "image"),
        "js": dir(root / "js"),
        "media": dir(root / "media"),
        "redirects.caddy": caddy_redirects(redirects),
        "robots.txt": file(root / "robots.txt"),
        **index(
            dict(
                # .md files get processed with page()
                (
                    (
                        str(path.relative_to(root / "pages").with_suffix(".html"))
                        if path.name == "index.md"
                        else f"{path.relative_to(root / 'pages').with_suffix('')}/"
                    ),
                    page(path),
                )
                if path.suffix == ".md"
                # other extensions get processed with file()
                else (str(path.relative_to(root / "pages")), file(path))
                for path in sorted(root.glob("pages/**"))
                if path.is_file()
            ),
            "poetry",
            "tools",
        ),
        "projects/colorby/": page(root / "projects/colorby/README.md", title="Colorby"),
        "projects/lumeh.org/": page(root / "README.md", title="lumeh.org"),
        "projects/pchyme/": page(root / "projects/pchyme/README.md", title="pchyme"),
        "projects/rockuefort/": page(
            root / "projects/rockuefort/README.md", title="Rockuefort"
        ),
        "projects/sfago2024.org/": page(root / "projects/sfago2024.org.md"),
        "projects/slideception/": page(
            root / "projects/slideception/README.md", title="slideception"
        ),
        "projects/thinking-green/": page(
            root / "projects/thinking-green/README.md", title="Thinking Green"
        ),
        "projects/voidpop/": page(root / "projects/voidpop/README.md", title="Voidpop"),
        "projects/websleydale/": page(root / "projects/websleydale.md"),
        **index(
            {
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
                    "spiced_spinach",
                    "sweet_potato_casserole",
                    "thai_chicken_curry",
                ]
            },
            "recipes",
        ),
    },
    redirects=redirects,
)
