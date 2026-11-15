# Switch language with this constant only: "fr" or "en".
LANG = "en"

FR = {
    "title": "FieldTank",
    "tag": "Cinq saisons. Chaque chiffre vient d'un fichier.",
    "pick_goal": "Choisis un objectif",
    "goal_yield": "Maximiser le rendement",
    "goal_water": "Economiser l'eau",
    "goal_stress": "Zero stress pour les plantes",
    "goal_yield_hint": "Score = rendement relatif",
    "goal_water_hint": "Score = rendement - 0,4 x irrigation mm",
    "goal_stress_hint": "Score = rendement - 1,5 x jours de stress",
    "btn_assumptions": "Hypotheses",
    "btn_credits": "Credits",
    "btn_back": "Retour",
    "btn_continue": "Continuer",
    "btn_replay": "Rejouer",
    "btn_next": "Saison suivante",
    "btn_final": "Voir le bilan",
    "btn_over": "La ferme ne tient pas",
    "season": "Saison {n}/{total}",
    "season_idle": "Saison 0/{total}",
    "hearts_label": "Coeurs",
    "xp_label": "Saisons terminees",
    "intro_rain": "Pluie (fichier) : {mm} mm",
    "intro_hot": "Jours chauds (fichier) : {n}",
    "intro_cap": "Capacite du sol (fichier) : {mm} mm",
    "intro_lat": "Latitude (fichier) : {lat}",
    "q0": "Quelle culture semer sans irrigation ?",
    "q1": "Faut-il irriguer le mais ?",
    "q2": "Quelle culture semer avec irrigation ?",
    "q3": "Faut-il irriguer le soja ?",
    "q4": "Quelle culture, et irriguer ou non ?",
    "slot": "Touche {k}",
    "irr_yes": "avec irrigation",
    "irr_no": "sans irrigation",
    "option": "{crop} — {irr}",
    "sat_label": "Example satellite view (GOES-16, 1 Jul 2024, ~2 km pixels), not from this season",
    "sat_file_time": "time_utc (fichier) : {t}",
    "sat_file_source": "source (fichier) : {s}",
    "sat_file_note": "note (fichier) : {s}",
    "sat_file_area": "approx_area_estimate (fichier) : {s}",
    "sat_hover": "row {r}, column {c}: {cels} degrees C ({kelvin} K)",
    "sat_cloud": "row {r}, column {c}: no data",
    "sat_hint": "Survole un pixel.",
    "sat_hot": "Contour : 10 % les plus chauds, seuil {cut} K (calcule sur les pixels non nuls).",
    "sat_nulls": "Pixels sans donnee : {n} / {total}",
    "sat_range": "{lo} °C  …  {hi} °C",
    "day": "Jour {n}",
    "day_note": "Un point de water_curve tous les 3 jours depuis le semis.",
    "tank": "Eau du sol",
    "tank_unit": "{v} % de la capacite",
    "soil_rule": "Affichage : >= 50 ok, 20 a 49 sec, < 20 fissure. Seuil de stress du modele : 50 %.",
    "anim_irr": "Animation. Irrigation totale (fichier) : {mm} mm.",
    "anim_heat": "Animation. Jours de chaleur (fichier) : {n}.",
    "yield_now": "Rendu final selon yield_pct : {pct} (relatif).",
    "play_skip": "ESPACE pour passer",
    "mark_ok": "BON",
    "mark_bad": "ECART",
    "mark_best": "MEILLEUR",
    "result_title": "Resultat",
    "gap_line": "Ecart au meilleur propose : {gap}",
    "hearts_rule": "Regle du jeu : ecart <= 10 : 0 coeur ; <= 30 : 1 coeur ; au-dela : 2 coeurs.",
    "hearts_lost": "Coeurs perdus : {n}",
    "fact_min_file": "min_water_pct (fichier) : {v}",
    "fact_min_curve": "Minimum de water_curve (calcule) : {v}",
    "fact_stress": "stress_days (fichier) : {n}",
    "fact_irr": "irrigation_mm (fichier) : {n}",
    "fact_heat": "heat_days (fichier) : {n}",
    "fact_yield": "yield_pct (fichier) : {n} (relatif, pas des tonnes)",
    "chart_chosen": "Choix",
    "chart_best": "Meilleur propose",
    "chart_axis": "Jours depuis le semis",
    "col_crop": "Culture",
    "col_irr": "Irr.",
    "col_yield": "Rdt",
    "col_stress": "Str.",
    "col_heat": "Chal.",
    "col_imm": "mm",
    "col_score": "Score",
    "col_offer": "Propose",
    "yes": "oui",
    "no": "non",
    "offered_yes": "oui",
    "offered_no": "non",
    "lesson_pair": "Irriguer {crop} : yield_pct {dy} points vs sans irrigation, stress_days economises {ds}. Ecart de score meilleur/pire (toutes options) : {spread}.",
    "lesson_spread": "Ecart de score meilleur/pire (toutes options) : {spread}.",
    "sam_happy": "Content",
    "sam_neutral": "Neutre",
    "sam_worried": "Inquiet",
    "mood_rule": "Humeur : ecart 0 content, <= 30 neutre, sinon inquiet.",
    "final_mood_rule": "Humeur finale : ecart total <= 10 content, <= 50 neutre, sinon inquiet.",
    "holds": "La ferme tient.",
    "not_holds": "La ferme ne tient pas.",
    "harvest": "Bilan",
    "total_line": "Total des scores : {got} / meilleur plan propose {best}",
    "total_gap": "Ecart total : {gap}",
    "hist_season": "Saison {n}",
    "hist_choice": "Choix : {label}",
    "hist_score": "Score {got} / meilleur {best}",
    "replay_hint": "Rejouer remet les coeurs a 5. Les chiffres ne changent pas.",
    "error_title": "Fichier de simulation illisible",
    "error_hint": "Place scenes.json a la racine ou dans data/. Le jeu n'invente aucun chiffre.",
    "assumptions_title": "Hypotheses",
    "assumptions_body": (
        "Sol gNATSGO, meteo Daymet. Bilan hydrique journalier simplifie "
        "(ET0 Hargreaves, coefficients culturaux FAO-56, rendement relatif FAO). "
        "Eau du sol initiale : 80 % de la capacite. Irrigation automatique de 25 mm "
        "quand le stress commence, maximum 100 mm par saison. Penalite chaleur : "
        "1 % de rendement par jour au-dessus du seuil de la culture (hypothese du projet, pas FAO). "
        "Le rendement est RELATIF (pas comparable en tonnes ni en argent entre cultures). "
        "Le panneau satellite est un exemple, un seul instantane. "
        "Simulation, pas un conseil agronomique."
    ),
    "credits_title": "Credits",
    "credits_missing": "assets/CREDITS.txt est absent.",
    "font_note": "Police : Press Start 2P si le fichier est present, sinon police pygame.",
    "manifest_warn": "Manifeste ou sprite ignore : {msg}",
    "key_help": "1-6 choisir  |  Entree continuer  |  Espace passer la saison  |  F1 hypotheses  |  F2 credits  |  F11 plein ecran  |  Echap quitter",
}

EN = {
    "title": "FieldTank",
    "tag": "Five seasons. Every number comes from a file.",
    "pick_goal": "Pick a goal",
    "goal_yield": "Maximiser le rendement",
    "goal_water": "Economiser l'eau",
    "goal_stress": "Zero stress pour les plantes",
    "goal_yield_hint": "Score = relative yield",
    "goal_water_hint": "Score = yield - 0.4 x irrigation mm",
    "goal_stress_hint": "Score = yield - 1.5 x stress days",
    "btn_assumptions": "Assumptions",
    "btn_credits": "Credits",
    "btn_back": "Back",
    "btn_continue": "Continue",
    "btn_replay": "Replay",
    "btn_next": "Next season",
    "btn_final": "See the tally",
    "btn_over": "The farm does not hold",
    "season": "Season {n}/{total}",
    "season_idle": "Season 0/{total}",
    "hearts_label": "Hearts",
    "xp_label": "Seasons completed",
    "intro_rain": "Rain (file): {mm} mm",
    "intro_hot": "Hot days (file): {n}",
    "intro_cap": "Soil capacity (file): {mm} mm",
    "intro_lat": "Latitude (file): {lat}",
    "q0": "Which crop do you sow without irrigation?",
    "q1": "Do you irrigate the maize?",
    "q2": "Which crop do you sow and irrigate?",
    "q3": "Do you irrigate the soybean?",
    "q4": "Which crop, and do you irrigate?",
    "slot": "Key {k}",
    "irr_yes": "irrigated",
    "irr_no": "not irrigated",
    "option": "{crop} — {irr}",
    "sat_label": "Example satellite view (GOES-16, 1 Jul 2024, ~2 km pixels), not from this season",
    "sat_file_time": "time_utc (file): {t}",
    "sat_file_source": "source (file): {s}",
    "sat_file_note": "note (file): {s}",
    "sat_file_area": "approx_area_estimate (file): {s}",
    "sat_hover": "row {r}, column {c}: {cels} degrees C ({kelvin} K)",
    "sat_cloud": "row {r}, column {c}: no data",
    "sat_hint": "Hover a pixel.",
    "sat_hot": "Outline: hottest 10%, cutoff {cut} K (computed on non-null pixels).",
    "sat_nulls": "No-data pixels: {n} / {total}",
    "sat_range": "{lo} C  …  {hi} C",
    "day": "Day {n}",
    "day_note": "One water_curve value every 3 days from sowing.",
    "tank": "Soil water",
    "tank_unit": "{v} % of capacity",
    "soil_rule": "Display: >= 50 ok, 20 to 49 dry, < 20 cracked. Model stress threshold: 50%.",
    "anim_irr": "Animation. Season irrigation total (file): {mm} mm.",
    "anim_heat": "Animation. Heat days (file): {n}.",
    "yield_now": "Final look uses yield_pct: {pct} (relative).",
    "play_skip": "SPACE to skip",
    "mark_ok": "BEST",
    "mark_bad": "GAP",
    "mark_best": "BEST",
    "result_title": "Result",
    "gap_line": "Gap to the best offered score: {gap}",
    "hearts_rule": "Game rule: gap <= 10: 0 hearts; <= 30: 1 heart; above that: 2 hearts.",
    "hearts_lost": "Hearts lost: {n}",
    "fact_min_file": "min_water_pct (file): {v}",
    "fact_min_curve": "Minimum of water_curve (computed): {v}",
    "fact_stress": "stress_days (file): {n}",
    "fact_irr": "irrigation_mm (file): {n}",
    "fact_heat": "heat_days (file): {n}",
    "fact_yield": "yield_pct (file): {n} (relative, not tonnes)",
    "chart_chosen": "Choice",
    "chart_best": "Best offered",
    "chart_axis": "Days since sowing",
    "col_crop": "Crop",
    "col_irr": "Irr.",
    "col_yield": "Yld",
    "col_stress": "Str.",
    "col_heat": "Heat",
    "col_imm": "mm",
    "col_score": "Score",
    "col_offer": "Offered",
    "yes": "yes",
    "no": "no",
    "offered_yes": "yes",
    "offered_no": "no",
    "lesson_pair": "Irrigating {crop}: yield_pct {dy} points versus dry, stress_days saved {ds}. Best/worst score spread (all options): {spread}.",
    "lesson_spread": "Best/worst score spread (all options): {spread}.",
    "sam_happy": "Happy",
    "sam_neutral": "Neutral",
    "sam_worried": "Worried",
    "mood_rule": "Mood: gap 0 happy, <= 30 neutral, otherwise worried.",
    "final_mood_rule": "Final mood: total gap <= 10 happy, <= 50 neutral, otherwise worried.",
    "holds": "The farm holds.",
    "not_holds": "The farm does not hold.",
    "harvest": "Tally",
    "total_line": "Score total: {got} / best offered plan {best}",
    "total_gap": "Total gap: {gap}",
    "hist_season": "Season {n}",
    "hist_choice": "Choice: {label}",
    "hist_score": "Score {got} / best {best}",
    "replay_hint": "Replay resets hearts to 5. The numbers do not change.",
    "error_title": "Simulation file cannot be read",
    "error_hint": "Put scenes.json in the project root or in data/. The game invents no numbers.",
    "assumptions_title": "Assumptions",
    "assumptions_body": (
        "Soil gNATSGO, weather Daymet. Simplified daily water balance "
        "(Hargreaves ET0, FAO-56 crop coefficients, FAO relative-yield method). "
        "Initial soil water 80% of capacity. Automatic irrigation of 25 mm when stress starts, "
        "max 100 mm per season. Heat penalty of 1% yield per day above the crop's threshold "
        "(a project assumption, not FAO). Yield is RELATIVE (not comparable in tonnes or money "
        "between crops). The satellite panel is one example snapshot. Simulation, not agronomic advice."
    ),
    "credits_title": "Credits",
    "credits_missing": "assets/CREDITS.txt is missing.",
    "font_note": "Font: Press Start 2P if the file is present, otherwise the pygame default.",
    "manifest_warn": "Manifest or sprite skipped: {msg}",
    "key_help": "1-6 choose  |  Enter continue  |  Space skip season  |  F1 assumptions  |  F2 credits  |  F11 fullscreen  |  Esc quit",
}


def t(key, **kw):
    table = FR if LANG == "fr" else EN
    text = table[key]
    if not kw:
        return text
    return text.format(**kw)


def question_text(index):
    return t("q%d" % index)


def irr_text(flag):
    return t("irr_yes") if flag else t("irr_no")


def option_label(choice):
    return t("option", crop=choice["crop"], irr=irr_text(choice["irrigate"]))


def fmt_num(value):
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        rounded = round(value, 4)
        if rounded == int(rounded):
            return str(int(rounded))
        return ("%.4f" % rounded).rstrip("0").rstrip(".")
    return str(value)
