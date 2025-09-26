import logging
from os.path import splitext
from pathlib import Path

from websleydale import (
    Author,
    Redirect,
    caddy_redirects,
    dir,
    file,
    formathtml,
    index,
    jinja,
    markdown,
    merge,
    sass,
    textmex,
)
from websleydale import (
    build as websleydale_build,
)

from .renderer import process_config, render_config


def textmex_page(source, *, title: str | None = None):
    return formathtml(
        jinja(
            textmex(source, process_config, render_config),
            template="page.html",
            title=title,
        )
    )


def page(source, *, title: str | None = None):
    return formathtml(jinja(markdown(source), template="page.html", title=title))


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


def build():
    root = Path(".")
    src = root / "src"
    websleydale_build(
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
            "css/lumeh.css": sass(src / "css/lumeh.sass"),
            "files": dir(root / "assets/files", allow_missing=True),
            "font": merge(
                dir(src / "font"), dir(root / "assets/font", allow_missing=True)
            ),
            "guess": dir(src / "guess"),
            "image": dir(src / "image"),
            "js": dir(src / "js"),
            "media": dir(src / "media"),
            "redirects.caddy": caddy_redirects(redirects),
            "robots.txt": file(src / "robots.txt"),
            **index(
                dict(
                    # .md files get processed with page()
                    (
                        (
                            str(path.relative_to(src / "pages").with_suffix(".html"))
                            if path.name == "index.md"
                            else f"{path.relative_to(src / 'pages').with_suffix('')}/"
                        ),
                        page(path),
                    )
                    if path.suffix == ".md"
                    # other extensions get processed with file()
                    else (str(path.relative_to(src / "pages")), file(path))
                    for path in sorted(src.glob("pages/**"))
                    if path.is_file()
                ),
                "poetry",
                "tools",
            ),
            "projects/colorby/": page(
                src / "projects/colorby/README.md", title="Colorby"
            ),
            "projects/lumeh.org/": page(root / "README.md", title="lumeh.org"),
            "projects/pchyme/": page(src / "projects/pchyme/README.md", title="pchyme"),
            "projects/rockuefort/": page(
                src / "projects/rockuefort/README.md", title="Rockuefort"
            ),
            "projects/sfago2024.org/": page(src / "projects/sfago2024.org.md"),
            "projects/slideception/": page(
                src / "projects/slideception/README.md", title="slideception"
            ),
            "projects/thinking-green/": page(
                src / "projects/thinking-green/README.md", title="Thinking Green"
            ),
            "projects/voidpop/": page(
                src / "projects/voidpop/README.md", title="Voidpop"
            ),
            "projects/websleydale/": page(src / "projects/websleydale.md"),
            **index(
                {
                    f"recipes/{splitext(name)[0].replace('_', '-')}/": page(
                        src / f"projects/recipes/{name}"
                    )
                    if name.endswith(".md")
                    else textmex_page(src / f"projects/recipes/{name}")
                    for name in [
                        "almond_salad_dressing.md",
                        "apple_cider.md",
                        "apple_crisp.md",
                        "asparagus_mushroom_soup.md",
                        "banana_bread.md",
                        "bettys_chili.md",
                        "calico_beans.md",
                        "chana_masala.md",
                        "chana_masala_with_spice_kit.md",
                        "chancakes.md",
                        "chicken_curry.md",
                        "chicken_curry_v2.md",
                        "chickpeas_pressure_cooker.md",
                        "chili.md",
                        "chonklate_chip_cookies.md",
                        "christmas_anything.md",
                        "cookies.md",
                        "cottage_pie.md",
                        "creme_brulee_cheesecake.md",
                        "curry_chicken_pot_pie.md",
                        "dal.mex",
                        "first_watch_seasoning.md",
                        "green_bean_bundles.md",
                        "krishna_lunch_chili.md",
                        "lemonade.md",
                        "little_white_ball_cookies.md",
                        "mac_and_cheese.md",
                        "popovers.md",
                        "pumpkin_bread.md",
                        "quiche.md",
                        "salmon_pate.md",
                        "shortbread_cookies.md",
                        "spiced_spinach.md",
                        "sweet_potato_casserole.md",
                        "thai_chicken_curry.md",
                    ]
                },
                "recipes",
            ),
        },
        redirects=redirects,
    )
