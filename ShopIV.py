import os
import discord
from discord import ui
from discord.ext import commands
import sqlite3

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
DB_NAME = "economy.db"

# --- Dictionnaire des titres d'épisodes (1 à 25) ---
EPISODE_TITLES = {
    1: "Épisode 1 — L’Arche",
    2: "Épisode 2 — Les Terres Tempérées",
    3: "Épisode 3 — Les Premières Villes",
    4: "Épisode 4 — Le Registre des Dirigeants",
    5: "Épisode 5 — Le Premier Départ",
    6: "Épisode 6 — Le Grand Départ",
    7: "Épisode 7 — La Première Capitale",
    8: "Épisode 8 — Le Gardien des Arches",
    9: "Épisode 9 — Le Mystère des Arches",
    10: "Épisode 10 — Les Premières Conquêtes",
    11: "Épisode 11 — La Course aux Territoires",
    12: "Épisode 12 — La Première Décision",
    13: "Épisode 13 — Le Premier Affrontement",
    14: "Épisode 14 — Trop Tard",
    15: "Épisode 15 — Le Temps Joue Contre Toi",
    16: "Épisode 16 — Le Piège",
    17: "Épisode 17 — Seraph",
    18: "Épisode 18 — L’Expédition",
    19: "Épisode 19 — Le Vétéran",
    20: "Épisode 20 — Les Temples",
    21: "Épisode 21 — La Guerre des Temples",
    22: "Épisode 22 — L’Après-Bataille",
    23: "Épisode 23 — Une Réputation naissante",
    24: "Épisode 24 — Le Prix de la Progression",
    25: "Épisode 25 — Le Siège"
}

# --- Textes des histoires racontées par Guillaume (Épisodes 1 et 2 intégrés) ---
EPISODE_STORIES = {
    1: (
        "« La journée touchait à sa fin.\n\n"
        "Comme presque tous les soirs, le Voyageur traversait le vieux parc pour rentrer chez lui.\n"
        "Au centre se dressait une immense arche de pierre.\n"
        "Les enfants jouaient autour.\n"
        "Les adultes passaient devant sans même la regarder.\n"
        "Pour eux… Ce n’était qu’une vieille ruine.\n\n"
        "« Mon ballon ! »\n\n"
        "Une petite voix brisa le silence. Un ballon venait de rouler sous l’arche. Sans réfléchir, le Voyageur courut le récupérer. "
        "Il le ramassa, puis fit un pas pour revenir.\n\n"
        "Le vent s’arrêta. Plus un bruit. Il leva lentement les yeux. Le parc had disparu.\n"
        "À sa place… Une vaste route pavée traversait une immense plaine. Des caravanes avançaient lentement. Des marchands discutaient.\n"
        "Le Voyageur resta figé.\n\n"
        "Parmi les voyageurs, certains ne ressemblaient à aucun être qu’il avait déjà vu. Leurs traits rappelaient ceux de grands félins, "
        "pourtant personne ne semblait leur accorder le moindre regard. Pendant un instant, il se demanda s’il était en train de rêver.\n\n"
        "Des gardes escortaient les convois. Au loin, une immense cité dominait l’horizon. Tout autour, de nombreuses villes s’étendaient à perte de vue. "
        "Presque toutes arboraient une bannière flottant au-dessus de leurs remparts. Certaines laissaient s’élever d’épaisses colonnes de fumée, "
        "signe qu’une bataille venait d’éclater.\n\n"
        "Un marchand le regarda de la tête aux pieds :\n"
        "— Ces vêtements… Tu viens d’une Arche, n’est-ce pas ?\n\n"
        "Le Voyageur n’eut pas le temps de répondre. Une corne de guerre retentit. Tous les regards se tournèrent vers l’horizon.\n"
        "Au loin… Une immense armée avançait vers la cité. Les portes commencèrent à se refermer.\n\n"
        "Le marchand attrapa brusquement le bras du Voyageur :\n"
        "— Si tu veux vivre… ne reste pas ici ! »"
    ),
    2: (
        "« Le Voyageur suivit le vieil homme à travers les rues pavées.\n\n"
        "Tout lui semblait étrange. Son regard ne cessait de parcourir la cité.\n"
        "Des marchands installaient leurs étals. Des soldats patrouillaient le long des remparts.\n"
        "Parmi les habitants, certains avaient des traits félins. Ils échangeaient, travaillaient et riaient aux côtés des humains, comme si cela avait toujours été ainsi.\n"
        "Le Voyageur détourna un instant le regard, puis observa de nouveau. Il comprenait peu à peu que ce monde possédait ses propres règles.\n"
        "Des habitants poursuivaient leur journée comme si son arrivée n’avait rien d’exceptionnel.\n\n"
        "Le Voyageur observait chaque détail.\n"
        "— Où sommes-nous ?\n\n"
        "Le vieil homme esquissa un léger sourire.\n"
        "— Ici… tu te trouves dans les Terres Tempérées.\n\n"
        "Le Voyageur leva les yeux vers l’horizon. Les plaines verdoyantes semblaient s’étendre à l’infini.\n"
        "— Les Terres Tempérées ?\n"
        "Le vieil homme acquiesça.\n"
        "— Oui. Beaucoup pensent que ce monde s’arrête ici…\n"
        "Il marqua une courte pause.\n"
        "— Mais un jour, tu découvriras que ces terres ne sont qu’une partie d’un royaume bien plus vaste.\n\n"
        "Le Voyageur voulut poser une nouvelle question. Mais le vieil homme reprit sa marche.\n"
        "— Chaque chose en son temps.\n\n"
        "Après quelques instants, ils arrivèrent devant un immense bâtiment de pierre. Au-dessus de l’entrée était gravé un ancien symbole représentant une Arche.\n"
        "Le Voyageur s’arrêta.\n"
        "— Quel est cet endroit ?\n\n"
        "Le vieil homme posa sa main sur la porte.\n"
        "— C’est ici que commence le chemin de tous les nouveaux dirigeants.\n"
        "Il ouvrit lentement les grandes portes.\n"
        "— Entre. Ton voyage ne fait que commencer.\n\n"
        "Le Voyageur inspira profondément. Puis franchit le seuil.\n"
        "Sans le savoir… Il venait de faire son premier pas sur le chemin des dirigeants. »"
    ),
    3: "", 4: "", 5: "", 6: "", 7: "", 8: "", 9: "", 10: "",
    11: "", 12: "", 13: "", 14: "", 15: "", 16: "", 17: "", 18: "", 19: "", 20: "",
    21: "", 22: "", 23: "", 24: "", 25: ""
}

def get_episode_title(ep_num: int) -> str:
    return EPISODE_TITLES.get(ep_num, f"Épisode {ep_num}")

def format_currency(amount: int) -> str:
    return f"{amount:,} $".replace(",", " ")

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                wallet INTEGER DEFAULT 0,
                bank INTEGER DEFAULT 0,
                last_daily INTEGER DEFAULT 0,
                streak INTEGER DEFAULT 0
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                user_id INTEGER,
                item_name TEXT,
                quantity INTEGER DEFAULT 1,
                PRIMARY KEY (user_id, item_name)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS story_progress (
                user_id INTEGER,
                episode INTEGER,
                PRIMARY KEY (user_id, episode)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS shop_items (
                item_key TEXT PRIMARY KEY,
                name TEXT,
                price INTEGER,
                description TEXT,
                shop_type TEXT DEFAULT 'normal',
                episode INTEGER DEFAULT 0,
                required_role_id INTEGER DEFAULT NULL,
                role_to_give_id INTEGER DEFAULT NULL
            )
        """)
        
        cursor.execute("PRAGMA table_info(shop_items)")
        columns = [column[1] for column in cursor.fetchall()]
        if "shop_type" not in columns:
            cursor.execute("ALTER TABLE shop_items ADD COLUMN shop_type TEXT DEFAULT 'normal'")
        if "episode" not in columns:
            cursor.execute("ALTER TABLE shop_items ADD COLUMN episode INTEGER DEFAULT 0")
        if "required_role_id" not in columns:
            cursor.execute("ALTER TABLE shop_items ADD COLUMN required_role_id INTEGER DEFAULT NULL")
        if "role_to_give_id" not in columns:
            cursor.execute("ALTER TABLE shop_items ADD COLUMN role_to_give_id INTEGER DEFAULT NULL")

        cursor.execute("SELECT COUNT(*) FROM shop_items")
        if cursor.fetchone()[0] == 0:
            default_items = [
                ("A1", "👑 Rôle VIP", 5000, "Un statut de VIP sur le serveur.", "normal", 0, None, None),
                ("A2", "🎁 Boîte Mystère", 1000, "Contient une surprise aléatoire !", "normal", 0, None, None),
                ("SP1", "💎 Épée Légendaire", 25000, "Une arme surpuissante réservée aux VIP.", "special", 0, None, None)
            ]
            cursor.executemany("INSERT INTO shop_items (item_key, name, price, description, shop_type, episode, required_role_id, role_to_give_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", default_items)

        cursor.execute("DELETE FROM shop_items WHERE shop_type = 'episode'")
        
        episode_items = [
            ("EP1_1", "Ballon oublié [01]", 500, "Objet d'histoire essentiel.", "episode", 1, None, None),
            ("EP1_2", "Fragment d’Arche [01]", 500, "Objet d'histoire essentiel.", "episode", 1, None, None),
            ("EP1_3", "Éclat du Passage [01]", 500, "Objet d'histoire essentiel.", "episode", 1, None, None),
            ("EP1_4", "Premier Passage [01]", 500, "Objet d'histoire essentiel.", "episode", 1, None, None),
            
            ("EP2_1", "Pièce de la Cité [02]", 500, "Objet d'histoire essentiel.", "episode", 2, None, None),
            ("EP2_2", "Carte des Terres Tempérées [02]", 500, "Objet d'histoire essentiel.", "episode", 2, None, None),
            ("EP2_3", "Sceau de la Cité [02]", 500, "Objet d'histoire essentiel.", "episode", 2, None, None),
            ("EP2_4", "Première Installation [02]", 500, "Objet d'histoire essentiel.", "episode", 2, None, None),
            
            ("EP3_1", "Bannière de Ville [03]", 500, "Objet d'histoire essentiel.", "episode", 3, None, None),
            ("EP3_2", "Charte des Dirigeants [03]", 500, "Objet d'histoire essentiel.", "episode", 3, None, None),
            ("EP3_3", "Ordre de Bataille [03]", 500, "Objet d'histoire essentiel.", "episode", 3, None, None),
            ("EP3_4", "Premières Conquêtes [03]", 500, "Objet d'histoire essentiel.", "episode", 3, None, None),
            
            ("EP4_1", "Registre des Dirigeants [04]", 500, "Objet d'histoire essentiel.", "episode", 4, None, None),
            ("EP4_2", "Plume d’Inscription [04]", 500, "Objet d'histoire essentiel.", "episode", 4, None, None),
            ("EP4_3", "Encre des Fondateurs [04]", 500, "Objet d'histoire essentiel.", "episode", 4, None, None),
            ("EP4_4", "Nouvel Arrivant [04]", 500, "Objet d'histoire essentiel.", "episode", 4, None, None),
            
            ("EP5_1", "Compas d’Explorateur [05]", 500, "Objet d'histoire essentiel.", "episode", 5, None, None),
            ("EP5_2", "Décret de Fondation [05]", 500, "Objet d'histoire essentiel.", "episode", 5, None, None),
            ("EP5_3", "Acte de Capitale [05]", 500, "Objet d'histoire essentiel.", "episode", 5, None, None),
            ("EP5_4", "Vers un Nouveau Départ [05]", 500, "Objet d'histoire essentiel.", "episode", 5, None, None),
            
            ("EP6_1", "Bottes de Voyage [06]", 500, "Objet d'histoire essentiel.", "episode", 6, None, None),
            ("EP6_2", "Sac du Colon [06]", 500, "Objet d'histoire essentiel.", "episode", 6, None, None),
            ("EP6_3", "Permis de Colonisation [06]", 500, "Objet d'histoire essentiel.", "episode", 6, None, None),
            ("EP6_4", "Le Grand Départ [06]", 500, "Objet d'histoire essentiel.", "episode", 6, None, None),
            
            ("EP7_1", "Coffret du Fondateur [07]", 500, "Objet d'histoire essentiel.", "episode", 7, None, None),
            ("EP7_2", "Pierre de Fondation [07]", 500, "Objet d'histoire essentiel.", "episode", 7, None, None),
            ("EP7_3", "Sceau de la Capitale [07]", 500, "Objet d'histoire essentiel.", "episode", 7, None, None),
            ("EP7_4", "Première Capitale [07]", 500, "Objet d'histoire essentiel.", "episode", 7, None, None),
            
            ("EP8_1", "Clé des Arches [08]", 500, "Objet d'histoire essentiel.", "episode", 8, None, None),
            ("EP8_2", "Insigne du Gardien [08]", 500, "Objet d'histoire essentiel.", "episode", 8, None, None),
            ("EP8_3", "Relique des Arches [08]", 500, "Objet d'histoire essentiel.", "episode", 8, None, None),
            ("EP8_4", "Le Gardien des Arches [08]", 500, "Objet d'histoire essentiel.", "episode", 8, None, None),
            
            ("EP9_1", "Parchemin Ancien [09]", 500, "Objet d'histoire essentiel.", "episode", 9, None, None),
            ("EP9_2", "Chronique Ancienne [09]", 500, "Objet d'histoire essentiel.", "episode", 9, None, None),
            ("EP9_3", "Secret des Arches [09]", 500, "Objet d'histoire essentiel.", "episode", 9, None, None),
            ("EP9_4", "Le Mystère des Arches [09]", 500, "Objet d'histoire essentiel.", "episode", 9, None, None),
            
            ("EP10_1", "Première Bannière [10]", 500, "Objet d'histoire essentiel.", "episode", 10, None, None),
            ("EP10_2", "Carte Territoriale [10]", 500, "Objet d'histoire essentiel.", "episode", 10, None, None),
            ("EP10_3", "Sceau du Territoire [10]", 500, "Objet d'histoire essentiel.", "episode", 10, None, None),
            ("EP10_4", "Premières Conquêtes [10]", 500, "Objet d'histoire essentiel.", "episode", 10, None, None),
            
            ("EP11_1", "Monture d’Éclaireur [11]", 500, "Objet d'histoire essentiel.", "episode", 11, None, None),
            ("EP11_2", "Tambour de Guerre [11]", 500, "Objet d'histoire essentiel.", "episode", 11, None, None),
            ("EP11_3", "Échelle de Siège [11]", 500, "Objet d'histoire essentiel.", "episode", 11, None, None),
            ("EP11_4", "La Course aux Territoires [11]", 500, "Objet d'histoire essentiel.", "episode", 11, None, None),
            
            ("EP12_1", "Lame d’Avant-garde [12]", 500, "Objet d'histoire essentiel.", "episode", 12, None, None),
            ("EP12_2", "Carquois Militaire [12]", 500, "Objet d'histoire essentiel.", "episode", 12, None, None),
            ("EP12_3", "Étendard de Guerre [12]", 500, "Objet d'histoire essentiel.", "episode", 12, None, None),
            ("EP12_4", "Premier Engagement [12]", 500, "Objet d'histoire essentiel.", "episode", 12, None, None),
            
            ("EP13_1", "Casque du Vainqueur [13]", 500, "Objet d'histoire essentiel.", "episode", 13, None, None),
            ("EP13_2", "Porte Fortifiée [13]", 500, "Objet d'histoire essentiel.", "episode", 13, None, None),
            ("EP13_3", "Médaille de Victoire [13]", 500, "Objet d'histoire essentiel.", "episode", 13, None, None),
            ("EP13_4", "Première Victoire [13]", 500, "Objet d'histoire essentiel.", "episode", 13, None, None),
            
            ("EP14_1", "Balise de Campagne [14]", 500, "Objet d'histoire essentiel.", "episode", 14, None, None),
            ("EP14_2", "Plan de Manœuvre [14]", 500, "Objet d'histoire essentiel.", "episode", 14, None, None),
            ("EP14_3", "Boussole Stratégique [14]", 500, "Objet d'histoire essentiel.", "episode", 14, None, None),
            ("EP14_4", "Faire les Bons Choix [14]", 500, "Objet d'histoire essentiel.", "episode", 14, None, None),
            
            ("EP15_1", "Chronomètre de Campagne [15]", 500, "Objet d'histoire essentiel.", "episode", 15, None, None),
            ("EP15_2", "Rapport de Reconnaissance [15]", 500, "Objet d'histoire essentiel.", "episode", 15, None, None),
            ("EP15_3", "Itinéraire de Marche [15]", 500, "Objet d'histoire essentiel.", "episode", 15, None, None),
            ("EP15_4", "La Course Continue [15]", 500, "Objet d'histoire essentiel.", "episode", 15, None, None),
            
            ("EP16_1", "Piège Camouflé [16]", 500, "Objet d'histoire essentiel.", "episode", 16, None, None),
            ("EP16_2", "Cor de Retraite [16]", 500, "Objet d'histoire essentiel.", "episode", 16, None, None),
            ("EP16_3", "Manœuvre d’Embuscade [16]", 500, "Objet d'histoire essentiel.", "episode", 16, None, None),
            ("EP16_4", "Le Piège [16]", 500, "Objet d'histoire essentiel.", "episode", 16, None, None),
            
            ("EP17_1", "Anneau Ancien [17]", 500, "Objet d'histoire essentiel.", "episode", 17, None, None),
            ("EP17_2", "Outil de Seraph [17]", 500, "Objet d'histoire essentiel.", "episode", 17, None, None),
            ("EP17_3", "Coffre d’Expédition [17]", 500, "Objet d'histoire essentiel.", "episode", 17, None, None),
            ("EP17_4", "Les Premières Découvertes [17]", 500, "Objet d'histoire essentiel.", "episode", 17, None, None),
            
            ("EP18_1", "Lanterne d’Expédition [18]", 500, "Objet d'histoire essentiel.", "episode", 18, None, None),
            ("EP18_2", "Relique Exhumée [18]", 500, "Objet d'histoire essentiel.", "episode", 18, None, None),
            ("EP18_3", "Coffre Scellé [18]", 500, "Objet d'histoire essentiel.", "episode", 18, None, None),
            ("EP18_4", "Première Expédition [18]", 500, "Objet d'histoire essentiel.", "episode", 18, None, None),
            
            ("EP19_1", "Plastron Usé [19]", 500, "Objet d'histoire essentiel.", "episode", 19, None, None),
            ("EP19_2", "Médaille de Campagne [19]", 500, "Objet d'histoire essentiel.", "episode", 19, None, None),
            ("EP19_3", "Insigne du Vétéran [19]", 500, "Objet d'histoire essentiel.", "episode", 19, None, None),
            ("EP19_4", "Le Vétéran [19]", 500, "Objet d'histoire essentiel.", "episode", 19, None, None),
            
            ("EP20_1", "Cloche du Temple [20]", 500, "Objet d'histoire essentiel.", "episode", 20, None, None),
            ("EP20_2", "Relique Sacrée [20]", 500, "Objet d'histoire essentiel.", "episode", 20, None, None),
            ("EP20_3", "Emblème du Temple [20]", 500, "Objet d'histoire essentiel.", "episode", 20, None, None),
            ("EP20_4", "L’Éveil des Temples [20]", 500, "Objet d'histoire essentiel.", "episode", 20, None, None),
            
            ("EP21_1", "Bouclier de Siège [21]", 500, "Objet d'histoire essentiel.", "episode", 21, None, None),
            ("EP21_2", "Pierre du Temple [21]", 500, "Objet d'histoire essentiel.", "episode", 21, None, None),
            ("EP21_3", "Étendard du Temple [21]", 500, "Objet d'histoire essentiel.", "episode", 21, None, None),
            ("EP21_4", "La Guerre des Temples [21]", 500, "Objet d'histoire essentiel.", "episode", 21, None, None),
            
            ("EP22_1", "Œil de l’Éclaireur [22]", 500, "Objet d'histoire essentiel.", "episode", 22, None, None),
            ("EP22_2", "Repère Stratégique [22]", 500, "Objet d'histoire essentiel.", "episode", 22, None, None),
            ("EP22_3", "Plan d’Expansion [22]", 500, "Objet d'histoire essentiel.", "episode", 22, None, None),
            ("EP22_4", "Voir Plus Loin [22]", 500, "Objet d'histoire essentiel.", "episode", 22, None, None),
            
            ("EP23_1", "Lettre Scellée [23]", 500, "Objet d'histoire essentiel.", "episode", 23, None, None),
            ("EP23_2", "Message Diplomatique [23]", 500, "Objet d'histoire essentiel.", "episode", 23, None, None),
            ("EP23_3", "Pacte Inconnu [23]", 500, "Objet d'histoire essentiel.", "episode", 23, None, None),
            ("EP23_4", "Une Réputation naissante [23]", 500, "Objet d'histoire essentiel.", "episode", 23, None, None),
            
            ("EP24_1", "Chariot Marchand [24]", 500, "Objet d'histoire essentiel.", "episode", 24, None, None),
            ("EP24_2", "Caisse de Provision [24]", 500, "Objet d'histoire essentiel.", "episode", 24, None, None),
            ("EP24_3", "Cargaison Royale [24]", 500, "Objet d'histoire essentiel.", "episode", 24, None, None),
            ("EP24_4", "Le Prix de la Progression [24]", 500, "Objet d'histoire essentiel.", "episode", 24, None, None),
            
            ("EP25_1", "Roue de Chariot [25]", 500, "Objet d'histoire essentiel.", "episode", 25, None, None),
            ("EP25_2", "Cor de Siège [25]", 500, "Objet d'histoire essentiel.", "episode", 25, None, None),
            ("EP25_3", "Ordre de Défense [25]", 500, "Objet d'histoire essentiel.", "episode", 25, None, None),
            ("EP25_4", "Le Siège [25]", 500, "Objet d'histoire essentiel.", "episode", 25, None, None)
        ]
        cursor.executemany("INSERT INTO shop_items (item_key, name, price, description, shop_type, episode, required_role_id, role_to_give_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", episode_items)
        conn.commit()

def get_user(user_id: int):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT wallet, bank, last_daily, streak FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if not row:
            cursor.execute("INSERT INTO users (user_id, wallet, bank) VALUES (?, 0, 0)", (user_id,))
            conn.commit()
            return 0, 0, 0, 0
        return row

@bot.event
async def on_ready():
    init_db()
    bot.add_view(PersistentMerchantView())
    bot.add_view(PersistentTroubadourView())
    print(f"Connecté en tant que {bot.user} (ID: {bot.user.id})")
    try:
        synced = await bot.tree.sync()
        print(f"Synchronisé {len(synced)} commandes slash.")
    except Exception as e:
        print(e)
    print("Prêt !")

# --- SYSTÈME DE GUILLAUME LE TROUBADOUR (INTERFAÇAGE PAGINÉ) ---
class TroubadourPaginationView(ui.View):
    def __init__(self, member: discord.Member, current_ep: int = 1):
        super().__init__(timeout=120)
        self.member = member
        self.current_ep = current_ep
        self.update_components()

    def update_components(self):
        self.clear_items()

        prev_btn = ui.Button(label="◀️ Précédent", style=discord.ButtonStyle.secondary, disabled=(self.current_ep <= 1), row=0)
        prev_btn.callback = self.prev_callback
        self.add_item(prev_btn)

        page_indicator = ui.Button(label=f"Épisode {self.current_ep} / 25", style=discord.ButtonStyle.blurple, disabled=True, row=0)
        self.add_item(page_indicator)

        next_btn = ui.Button(label="Suivant ▶️", style=discord.ButtonStyle.secondary, disabled=(self.current_ep >= 25), row=0)
        next_btn.callback = self.next_callback
        self.add_item(next_btn)

        has_story = self.current_ep in EPISODE_STORIES and bool(EPISODE_STORIES[self.current_ep].strip())

        if not has_story:
            rest_btn = ui.Button(label="💤 Le troubadour se repose, revenez plus tard", style=discord.ButtonStyle.danger, disabled=True, row=1)
            self.add_item(rest_btn)
            return

        user_id = self.member.id
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM story_progress WHERE user_id = ? AND episode = ?", (user_id, self.current_ep))
            is_unlocked = cursor.fetchone() is not None

            if self.current_ep == 1:
                has_all_items = True
            else:
                prev_ep = self.current_ep - 1
                cursor.execute("SELECT name FROM shop_items WHERE shop_type='episode' AND episode=?", (prev_ep,))
                prev_ep_items = [row[0] for row in cursor.fetchall()]

                has_all_items = False
                if prev_ep_items:
                    cursor.execute("""
                        SELECT COUNT(*) FROM inventory 
                        WHERE user_id = ? AND item_name IN ({}) AND quantity > 0
                    """.format(','.join(['?']*len(prev_ep_items))), [user_id] + prev_ep_items)
                    owned_count = cursor.fetchone()[0]
                    if owned_count >= len(prev_ep_items):
                        has_all_items = True

        if is_unlocked:
            listen_btn = ui.Button(label="📖 Écouter / Relire l'histoire", style=discord.ButtonStyle.success, emoji="📜", row=1)
            listen_btn.callback = self.listen_callback
            self.add_item(listen_btn)
        elif self.current_ep == 1:
            listen_btn = ui.Button(label="📖 Écouter l'Histoire (Gratuit)", style=discord.ButtonStyle.success, emoji="📜", row=1)
            listen_btn.callback = self.listen_callback
            self.add_item(listen_btn)
        elif has_all_items:
            give_btn = ui.Button(label="🎁 Donner les reliques & Écouter", style=discord.ButtonStyle.primary, emoji="✨", row=1)
            give_btn.callback = self.give_callback
            self.add_item(give_btn)
        else:
            lock_btn = ui.Button(label="🔒 Épisode Verrouillé (Reliques précédentes manquantes)", style=discord.ButtonStyle.danger, disabled=True, row=1)
            self.add_item(lock_btn)

    async def prev_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.member.id:
            return await interaction.response.send_message("❌ Ce n'est pas votre tour !", ephemeral=True)
        if self.current_ep > 1:
            self.current_ep -= 1
            self.update_components()
            await interaction.response.edit_message(embed=self.build_embed(), view=self)

    async def next_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.member.id:
            return await interaction.response.send_message("❌ Ce n'est pas votre tour !", ephemeral=True)
        if self.current_ep < 25:
            self.current_ep += 1
            self.update_components()
            await interaction.response.edit_message(embed=self.build_embed(), view=self)

    async def listen_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.member.id:
            return await interaction.response.send_message("❌ Ce n'est pas votre tour !", ephemeral=True)
        
        story_text = EPISODE_STORIES.get(self.current_ep, "« Une histoire mystérieuse... »")
        extra_txt = " (Offert à tous les voyageurs !)" if self.current_ep == 1 else " (Vous possédez déjà cet épisode dans vos archives permanentes.)"
        
        embed = discord.Embed(
            title=f"📜 Récit de {get_episode_title(self.current_ep)}",
            description=f"{story_text}\n\n*✨ {extra_txt}*",
            color=discord.Color.gold()
        )
        embed.set_thumbnail(url="https://images.emojiterra.com/google/android-10/512px/1f3ad.png")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def give_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.member.id:
            return await interaction.response.send_message("❌ Ce n'est pas votre tour !", ephemeral=True)
        
        has_story = self.current_ep in EPISODE_STORIES and bool(EPISODE_STORIES[self.current_ep].strip())
        if not has_story:
            return await interaction.response.send_message("❌ Le troubadour se repose, revenez plus tard !", ephemeral=True)

        user_id = self.member.id
        prev_ep = self.current_ep - 1

        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM shop_items WHERE shop_type='episode' AND episode=?", (prev_ep,))
            prev_ep_items = [row[0] for row in cursor.fetchall()]

            cursor.execute("INSERT OR IGNORE INTO story_progress (user_id, episode) VALUES (?, ?)", (user_id, self.current_ep))

            for item in prev_ep_items:
                cursor.execute("DELETE FROM inventory WHERE user_id = ? AND item_name = ?", (user_id, item))
            conn.commit()

        self.update_components()
        story_text = EPISODE_STORIES.get(self.current_ep, "« Une histoire mystérieuse... »")
        
        embed = discord.Embed(
            title=f"📜 Récit de {get_episode_title(self.current_ep)}",
            description=f"{story_text}\n\n*✨ (Guillaume a pris vos reliques de l'épisode {prev_ep} et a sauvegardé cet épisode à vie dans vos archives !) *",
            color=discord.Color.gold()
        )
        embed.set_thumbnail(url="https://images.emojiterra.com/google/android-10/512px/1f3ad.png")
        
        await interaction.response.edit_message(embed=self.build_embed(), view=self)
        await interaction.followup.send(embed=embed, ephemeral=True)

    def build_embed(self) -> discord.Embed:
        has_story = self.current_ep in EPISODE_STORIES and bool(EPISODE_STORIES[self.current_ep].strip())

        if not has_story:
            status_txt = "💤 **[Le troubadour se repose, revenez plus tard]**"
        elif self.current_ep == 1:
            status_txt = "📖 **[Épisode Gratuit & Accessible]**"
        else:
            user_id = self.member.id
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1 FROM story_progress WHERE user_id = ? AND episode = ?", (user_id, self.current_ep))
                is_unlocked = cursor.fetchone() is not None

            status_txt = "📖 **[Débloqué & Sauvegardé]**" if is_unlocked else f"🔒 **[Verrouillé / Reliques de l'épisode {self.current_ep - 1} requises]**"

        embed = discord.Embed(
            title=f"🪕 Guillaume le Troubadour — {get_episode_title(self.current_ep)}",
            description=(
                f"Statut : {status_txt}\n\n"
                "Utilisez les boutons ci-dessous pour naviguer entre les épisodes, donner vos reliques ou écouter les récits de votre choix !"
            ),
            color=discord.Color.purple()
        )
        embed.set_thumbnail(url="https://images.emojiterra.com/google/android-10/512px/1f3ad.png")
        return embed

class PersistentTroubadourView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="Parler à Guillaume", style=discord.ButtonStyle.success, emoji="🪕", custom_id="persistent_troubadour_talk_main")
    async def talk_to_troubadour(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.defer(ephemeral=True)

        if not isinstance(interaction.user, discord.Member):
            return await interaction.followup.send("❌ Erreur.", ephemeral=True)

        view = TroubadourPaginationView(interaction.user, current_ep=1)
        await interaction.followup.send(embed=view.build_embed(), view=view, ephemeral=True)

# --- VUE POUR LA BOUTIQUE DES ÉPISODES ---
class EpisodeShopView(ui.View):
    def __init__(self, member: discord.Member, episode_num: int):
        super().__init__(timeout=120)
        self.member = member
        self.episode_num = episode_num
        self.load_items()

    def load_items(self):
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT item_key, name, price FROM shop_items WHERE shop_type = 'episode' AND episode = ?", (self.episode_num,))
            items = cursor.fetchall()

        all_bought = True
        for item_key, name, price in items:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT quantity FROM inventory WHERE user_id=? AND item_name=?", (self.member.id, name))
                res = cursor.fetchone()
                has_item = bool(res and res[0] > 0)

            owned = has_item

            if not owned:
                all_bought = False

            button = ui.Button(
                label=f"Possédé : {name}" if owned else f"Acheter {name} ({format_currency(price)})",
                style=discord.ButtonStyle.secondary if owned else discord.ButtonStyle.success,
                custom_id=f"ep_buy_{item_key}_{self.episode_num}",
                disabled=owned,
                row=0
            )
            button.callback = self.create_callback(item_key, name, price)
            self.add_item(button)

        if all_bought and len(items) > 0 and self.episode_num < 25:
            next_btn = ui.Button(
                label="➡️ Épisode Suivant", 
                style=discord.ButtonStyle.primary, 
                custom_id=f"next_ep_{self.episode_num}",
                row=1
            )
            next_btn.callback = self.next_episode_callback
            self.add_item(next_btn)

    def create_callback(self, item_key: str, item_name: str, item_price: int):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.member.id:
                return await interaction.response.send_message("❌ Ce n'est pas votre boutique !", ephemeral=True)
            
            wallet, _, _, _ = get_user(self.member.id)
            if wallet < item_price:
                return await interaction.response.send_message(f"❌ Solde insuffisant ! Il te manque {format_currency(item_price - wallet)}.", ephemeral=True)

            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET wallet = wallet - ? WHERE user_id = ?", (item_price, self.member.id))
                cursor.execute("""
                    INSERT INTO inventory (user_id, item_name, quantity) VALUES (?, ?, 1)
                    ON CONFLICT(user_id, item_name) DO UPDATE SET quantity = quantity + 1
                """, (self.member.id, item_name))
                conn.commit()

            new_view = EpisodeShopView(self.member, self.episode_num)
            
            title = get_episode_title(self.episode_num)
            embed = discord.Embed(title=f"📜 {title}", color=discord.Color.dark_teal())
            embed.description = "Achète tous les objets de cet épisode !"
            
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name, price, description FROM shop_items WHERE shop_type='episode' AND episode=?", (self.episode_num,))
                items = cursor.fetchall()
                
            for n, p, desc in items:
                embed.add_field(name=n, value=f"Prix : **{format_currency(p)}**\n*{desc}*", inline=False)
            
            await interaction.response.edit_message(embed=embed, view=new_view)
            await interaction.followup.send(f"✅ Tu as acheté **{item_name}** pour {format_currency(item_price)} !", ephemeral=True)
        return callback

    async def next_episode_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.member.id:
            return await interaction.response.send_message("❌ Ce n'est pas votre boutique !", ephemeral=True)
        
        next_ep = self.episode_num + 1
        new_view = EpisodeShopView(self.member, next_ep)
        
        title = get_episode_title(next_ep)
        embed = discord.Embed(title=f"📜 {title}", color=discord.Color.dark_teal())
        embed.description = "Achète tous les objets de cet épisode !"
        
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, price, description FROM shop_items WHERE shop_type='episode' AND episode=?", (next_ep,))
            items = cursor.fetchall()
            
        for n, p, desc in items:
            embed.add_field(name=n, value=f"Prix : **{format_currency(p)}**\n*{desc}*", inline=False)
        
        await interaction.response.edit_message(embed=embed, view=new_view)

# --- VUE POUR LA BOUTIQUE DYNAMIQUE CLASSIQUE ---
class DynamicShopView(ui.View):
    def __init__(self, member: discord.Member, shop_type: str):
        super().__init__(timeout=60)
        self.member = member
        self.shop_type = shop_type
        self.load_items()

    def load_items(self):
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT item_key, name, price, required_role_id FROM shop_items WHERE shop_type = ?", (self.shop_type,))
            items = cursor.fetchall()

        for item_key, name, price, required_role_id in items:
            if required_role_id is not None:
                role = self.member.guild.get_role(required_role_id)
                if not role or role not in self.member.roles:
                    continue

            button = ui.Button(
                label=f"Acheter {name} ({format_currency(price)})",
                style=discord.ButtonStyle.success,
                custom_id=f"shop_buy_{item_key}"
            )
            button.callback = self.create_callback(item_key)
            self.add_item(button)

    def create_callback(self, item_key: str):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.member.id:
                return await interaction.response.send_message("❌ Ce n'est pas votre boutique !", ephemeral=True)
            
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name, price, role_to_give_id FROM shop_items WHERE item_key = ?", (item_key,))
                item = cursor.fetchone()

            if not item:
                return await interaction.response.send_message("❌ Cet article n'existe plus.", ephemeral=True)

            item_name, item_price, role_to_give_id = item
            wallet, _, _, _ = get_user(self.member.id)

            if wallet < item_price:
                return await interaction.response.send_message(f"❌ Solde insuffisant ! Il te manque {format_currency(item_price - wallet)}.", ephemeral=True)

            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET wallet = wallet - ? WHERE user_id = ?", (item_price, self.member.id))
                cursor.execute("""
                    INSERT INTO inventory (user_id, item_name, quantity) VALUES (?, ?, 1)
                    ON CONFLICT(user_id, item_name) DO UPDATE SET quantity = quantity + 1
                """, (self.member.id, item_name))
                conn.commit()

            feedback_extra = ""
            if role_to_give_id:
                role_to_give = interaction.guild.get_role(role_to_give_id)
                if role_to_give:
                    try:
                        await self.member.add_roles(role_to_give)
                        feedback_extra = f" et le rôle **{role_to_give.name}** t'a été attribué !"
                    except discord.Forbidden:
                        feedback_extra = "\n⚠️ *Achat réussi, mais le bot manque de permissions pour attribuer le rôle.*"

            await interaction.response.send_message(f"✅ Achat réussi ! Tu as acheté **{item_name}** pour {format_currency(item_price)}{feedback_extra}", ephemeral=True)
        return callback

# --- MENU DE DIALOGUE PRINCIPAL DU MARCHAND ---
class ShopDialogueView(ui.View):
    def __init__(self, member: discord.Member):
        super().__init__(timeout=120)
        self.member = member
        
        has_special_access = False
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT required_role_id FROM shop_items WHERE shop_type = 'special'")
            rows = cursor.fetchall()
            for row in rows:
                r_id = row[0]
                if r_id:
                    r = self.member.guild.get_role(r_id)
                    if r and r in self.member.roles:
                        has_special_access = True
                        break

        if has_special_access:
            special_button = ui.Button(
                label="✨ Boutique Spéciale (Inédits)",
                style=discord.ButtonStyle.blurple,
                custom_id="shop_dialogue_special"
            )
            special_button.callback = self.open_special_shop
            self.add_item(special_button)

    @ui.button(label="🛒 Voir la boutique", style=discord.ButtonStyle.primary, emoji="✨", custom_id="shop_dialogue_browse")
    async def open_shop(self, interaction: discord.Interaction, button: ui.Button):
        if interaction.user.id != self.member.id:
            return await interaction.response.send_message("❌ Ce n'est pas ton tour de parler au marchand !", ephemeral=True)
        
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, price, description, required_role_id FROM shop_items WHERE shop_type = 'normal'")
            items = cursor.fetchall()

        embed = discord.Embed(title="🛒 Boutique Normale", color=discord.Color.gold())
        embed.description = "Voici les objets disponibles :"

        for name, price, desc, required_role_id in items:
            embed.add_field(name=name, value=f"Prix : **{format_currency(price)}**\n*{desc}*", inline=False)

        view = DynamicShopView(interaction.user, 'normal')
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @ui.button(label="📖 Boutique Histoire", style=discord.ButtonStyle.success, emoji="📜", custom_id="shop_dialogue_story")
    async def open_story_shop(self, interaction: discord.Interaction, button: ui.Button):
        if interaction.user.id != self.member.id:
            return await interaction.response.send_message("❌ Ce n'est pas ton tour !", ephemeral=True)
            
        current_ep = 1
        view = EpisodeShopView(interaction.user, current_ep)
        title = get_episode_title(current_ep)
        embed = discord.Embed(title=f"📜 {title}", color=discord.Color.dark_teal())
        embed.description = "Achète tous les objets de cet épisode !"
        
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, price, description FROM shop_items WHERE shop_type='episode' AND episode=?", (current_ep,))
            items = cursor.fetchall()
            
        for name, price, desc in items:
            embed.add_field(name=name, value=f"Prix : **{format_currency(price)}**\n*{desc}*", inline=False)

        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    async def open_special_shop(self, interaction: discord.Interaction):
        if interaction.user.id != self.member.id:
            return await interaction.response.send_message("❌ Ce n'est pas ton tour !", ephemeral=True)

        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, price, description FROM shop_items WHERE shop_type = 'special'")
            items = cursor.fetchall()

        embed = discord.Embed(title="✨ Boutique Spéciale & Inédite", color=discord.Color.purple())
        embed.description = "Félicitations pour ton accès exclusif ! Voici les articles inédits :"

        for name, price, desc in items:
            embed.add_field(name=name, value=f"Prix : **{format_currency(price)}**\n*{desc}*", inline=False)

        view = DynamicShopView(interaction.user, 'special')
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @ui.button(label="🎒 Voir mon inventaire", style=discord.ButtonStyle.secondary, emoji="📦", custom_id="shop_dialogue_inventory")
    async def open_inventory(self, interaction: discord.Interaction, button: ui.Button):
        if interaction.user.id != self.member.id:
            return await interaction.response.send_message("❌ Ce n'est pas ton tour de parler au marchand !", ephemeral=True)
        
        user_id = interaction.user.id
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT item_name, quantity FROM inventory WHERE user_id = ?", (user_id,))
            rows = cursor.fetchall()

        embed = discord.Embed(title=f"🎒 Inventaire de {interaction.user.display_name}", color=discord.Color.blue())
        if not rows:
            embed.description = "Ton inventaire est désespérément vide..."
        else:
            description = [f"• **{item_name}** x`{qty}`" for item_name, qty in rows]
            embed.description = "\n".join(description)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @ui.button(label="👋 Au revoir !", style=discord.ButtonStyle.danger, emoji="🚪", custom_id="shop_dialogue_leave")
    async def leave_chat(self, interaction: discord.Interaction, button: ui.Button):
        if interaction.user.id != self.member.id:
            return await interaction.response.send_message("❌ Ce n'est pas ton tour !", ephemeral=True)
        await interaction.response.defer()
        await interaction.delete_original_response()

class PersistentMerchantView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="Parler au Marchand", style=discord.ButtonStyle.success, emoji="🦊", custom_id="persistent_merchant_talk_main")
    async def talk_to_merchant(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.defer(ephemeral=True)

        if not isinstance(interaction.user, discord.Member):
            return await interaction.followup.send("❌ Erreur.", ephemeral=True)

        embed = discord.Embed(
            title="🦊 Tom - Le Marchand Ambulant",
            description=(
                f"Oh, bonjour **{interaction.user.display_name}** ! "
                "Bienvenue dans ma boutique exclusive !\n\n"
                "*Qu'est-ce qui t'amène par ici aujourd'hui ? Fais ton choix camarade...*"
            ),
            color=discord.Color.orange()
        )
        embed.set_thumbnail(url="https://images.emojiterra.com/google/android-10/512px/1f98a.png")

        view = ShopDialogueView(interaction.user)
        await interaction.followup.send(embed=embed, view=view, ephemeral=True)

@bot.tree.command(name="balance", description="Vérifie ton solde ou celui d'un autre utilisateur")
async def balance(interaction: discord.Interaction, member: discord.Member = None):
    target = member or interaction.user
    wallet, bank, _, _ = get_user(target.id)
    embed = discord.Embed(title=f"Portefeuille de {target.display_name}", color=discord.Color.blurple())
    embed.add_field(name="Portefeuille", value=format_currency(wallet), inline=True)
    embed.add_field(name="Banque", value=format_currency(bank), inline=True)
    embed.set_thumbnail(url=target.display_avatar.url)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="setup-marchand", description="[Admin] Installe le PNJ permanent dans le salon actuel")
@commands.has_permissions(administrator=True)
async def setup_marchand(interaction: discord.Interaction):
    embed = discord.Embed(
        title="✨ Bienvenue au Salon du Shop !",
        description=(
            "🦊 **Tom le Marchand** est installé ici en permanence.\n\n"
            "👉 **Clique sur le bouton ci-dessous** pour engager la discussion avec lui !"
        ),
        color=discord.Color.gold()
    )
    embed.set_thumbnail(url="https://images.emojiterra.com/google/android-10/512px/1f98a.png")
    view = PersistentMerchantView()
    await interaction.channel.send(embed=embed, view=view)
    await interaction.response.send_message("✅ Le PNJ marchand a été installé avec succès dans ce salon !", ephemeral=True)

@setup_marchand.error
async def setup_marchand_error(interaction: discord.Interaction, error):
    if isinstance(error, discord.app_commands.MissingPermissions):
        await interaction.response.send_message("❌ Permission refusée.", ephemeral=True)
    else:
        await interaction.response.send_message(f"❌ Erreur : {error}", ephemeral=True)

@bot.tree.command(name="setup-troubadour", description="[Admin] Installe Guillaume le Troubadour permanent dans le salon actuel")
@commands.has_permissions(administrator=True)
async def setup_troubadour(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🪕 Guillaume le Troubadour",
        description=(
            "✨ **Guillaume** est arrivé pour conter les épopées de vos voyages.\n\n"
            "👉 **Clique sur le bouton ci-dessous** pour lui parler et lui donner vos reliques d'épisodes !"
        ),
        color=discord.Color.purple()
    )
    embed.set_thumbnail(url="https://images.emojiterra.com/google/android-10/512px/1f3ad.png")
    view = PersistentTroubadourView()
    await interaction.channel.send(embed=embed, view=view)
    await interaction.response.send_message("✅ Guillaume le Troubadour a été installé avec succès dans ce salon !", ephemeral=True)

@setup_troubadour.error
async def setup_troubadour_error(interaction: discord.Interaction, error):
    if isinstance(error, discord.app_commands.MissingPermissions):
        await interaction.response.send_message("❌ Permission refusée.", ephemeral=True)
    else:
        await interaction.response.send_message(f"❌ Erreur : {error}", ephemeral=True)

@bot.tree.command(name="reset-story", description="[Admin] Réinitialise la progression des histoires et supprime les reliques des inventaires")
@commands.has_permissions(administrator=True)
async def reset_story(interaction: discord.Interaction):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM story_progress")
        cursor.execute("DELETE FROM inventory WHERE item_name LIKE '%[%]%'")
        conn.commit()

    await interaction.response.send_message("🔄 **Réinitialisation réussie !** Toutes les histoires validées et les reliques d'épisodes ont été remises à zéro pour les tests.", ephemeral=True)

@reset_story.error
async def reset_story_error(interaction: discord.Interaction, error):
    if isinstance(error, discord.app_commands.MissingPermissions):
        await interaction.response.send_message("❌ Permission refusée.", ephemeral=True)
    else:
        await interaction.response.send_message(f"❌ Erreur : {error}", ephemeral=True)

@bot.tree.command(name="inventory", description="Affiche ton inventaire d'achats")
async def inventory(interaction: discord.Interaction):
    user_id = interaction.user.id
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT item_name, quantity FROM inventory WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()

    embed = discord.Embed(title=f"🎒 Inventaire de {interaction.user.display_name}", color=discord.Color.blue())
    if not rows:
        embed.description = "Ton inventaire est désespérément vide..."
    else:
        description = [f"• **{item_name}** x`{qty}`" for item_name, qty in rows]
        embed.description = "\n".join(description)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="shop_add", description="[Admin] Ajoute un article normal, spécial ou épisode")
@commands.has_permissions(administrator=True)
async def shop_add(
    interaction: discord.Interaction, 
    item_key: str, 
    name: str, 
    price: int, 
    description: str, 
    shop_type: str = "normal", 
    episode: int = 0,
    required_role: discord.Role = None, 
    role_to_give: discord.Role = None
):
    req_role_id = required_role.id if required_role else None
    give_role_id = role_to_give.id if role_to_give else None

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO shop_items (item_key, name, price, description, shop_type, episode, required_role_id, role_to_give_id) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(item_key) DO UPDATE SET 
                name = ?, price = ?, description = ?, shop_type = ?, episode = ?, required_role_id = ?, role_to_give_id = ?
        """, (item_key, name, price, description, shop_type, episode, req_role_id, give_role_id, 
              name, price, description, shop_type, episode, req_role_id, give_role_id))
        conn.commit()

    ep_txt = f" (Épisode {episode})" if shop_type == "episode" else ""
    await interaction.response.send_message(f"✅ L'article **{name}** a été ajouté au shop **{shop_type}**{ep_txt} avec succès !", ephemeral=True)

@shop_add.error
async def shop_add_error(interaction: discord.Interaction, error):
    if isinstance(error, discord.app_commands.MissingPermissions):
        await interaction.response.send_message("❌ Permission refusée.", ephemeral=True)
    else:
        await interaction.response.send_message(f"❌ Erreur : {error}", ephemeral=True)

@bot.tree.command(name="shop_remove", description="[Admin] Supprime un article de la boutique")
@commands.has_permissions(administrator=True)
async def shop_remove(interaction: discord.Interaction, item_key: str):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM shop_items WHERE item_key = ?", (item_key,))
        deleted = cursor.rowcount
        conn.commit()

    if deleted > 0:
        await interaction.response.send_message(f"✅ Article `{item_key}` supprimé.", ephemeral=True)
    else:
        await interaction.response.send_message(f"❌ Aucun article trouvé avec la clé `{item_key}`.", ephemeral=True)

@shop_remove.error
async def shop_remove_error(interaction: discord.Interaction, error):
    if isinstance(error, discord.app_commands.MissingPermissions):
        await interaction.response.send_message("❌ Permission refusée.", ephemeral=True)
    else:
        await interaction.response.send_message(f"❌ Erreur : {error}", ephemeral=True)

# Récupération sécurisée du token via la variable d'environnement Fly.io
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)