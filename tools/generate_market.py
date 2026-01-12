
import yaml
import os

# Configuration
DB_PATH = 'rAthena/db/pre-re/'
OUTPUT_PATH = 'rAthena/npc/custom/ravena_market.txt'

# Categories Definition
SHOPS = {
    # Weapons
    'Shop_Bows': [],
    'Shop_Instruments': [],
    'Shop_Whips': [],
    'Shop_1hSwords': [],
    'Shop_2hSwords': [],
    'Shop_Rods': [],
    'Shop_Maces': [],
    'Shop_Knuckles': [],
    'Shop_Books': [],
    'Shop_Daggers': [],
    'Shop_Spears': [],
    'Shop_Katars': [],
    'Shop_Axes': [],
    'Shop_Guns': [],
    'Shop_Huuma': [],
    'Shop_Shields_W': [], # Shields in Weapon NPC
    'Shop_Arrows': [],
    'Shop_Bullets': [],
    'Shop_Ninjas': [],
    
    # Armor
    'Shop_Body': [],
    'Shop_Robe': [],
    'Shop_Shoes': [],
    'Shop_Shields_A': [], # Shields in Armor NPC
    
    # Head
    'Shop_Head_Top': [],
    'Shop_Head_Mid': [],
    'Shop_Head_Low': [],
    
    # Accessories
    'Shop_Accessories': [],
    
    # Consumables
    'Shop_Health': [],
    'Shop_Buffs': [],
    'Shop_Scrolls': [],
    'Shop_Enchant': [],
    
    # Cards
    'Shop_Card_Weap': [],
    'Shop_Card_Shoe': [],
    'Shop_Card_Garm': [],
    'Shop_Card_Acc': [],
    'Shop_Card_Arm': [],
    'Shop_Card_Shld': [],
    'Shop_Card_Head': [],
    
    # Crafting
    'Shop_Forging': [],
    'Shop_Alchemy': [],
    'Shop_Gems': [],
    'Shop_Craft_Class': [],
    
    # Useful
    'Shop_Useful': []
}

# Counters to avoid huge shops (game limits)
# If a shop has > 100 items, maybe split? rAthena supports large shops but scrolling is annoying.
# Ghost shops don't have strict size limits like packet size, but client might lag.
# We will use the shop names as is.

def load_yaml(filename):
    path = os.path.join(DB_PATH, filename)
    print(f"Loading {path}...")
    with open(path, 'r', encoding='utf-8') as f:
        # Skip header until "Body:" if possible, or just safe_load the whole thing
        # The file format has 'Body' key.
        data = yaml.safe_load(f)
        return data.get('Body', [])

def process_items(items):
    for item in items:
        # Skip invalid items
        if not item or 'Id' not in item:
            continue
            
        item_id = item['Id']
        name = item.get('Name', '')
        aegis = item.get('AegisName', '')
        type_ = item.get('Type', '')
        subtype = item.get('SubType', '')
        locs = item.get('Locations', {})
        trade = item.get('Trade', {})
        
        # Check Trade restrictions
        # if trade.get('NoTrade') or trade.get('NoSell'):
        #    continue
        # User said "Basically EVERY ITEM". I will only exclude if NoTrade AND NoDrop to avoid quest items.
        # Actually, let's just exclude NoTrade.
        if trade and (trade.get('NoTrade') or trade.get('NoSell')):
            continue

        # -- Weapons --
        if type_ == 'Weapon':
            if subtype in ['Bow']: SHOPS['Shop_Bows'].append(item_id)
            elif subtype in ['Musical']: SHOPS['Shop_Instruments'].append(item_id)
            elif subtype in ['Whip']: SHOPS['Shop_Whips'].append(item_id)
            elif subtype in ['1hSword']: SHOPS['Shop_1hSwords'].append(item_id)
            elif subtype in ['2hSword']: SHOPS['Shop_2hSwords'].append(item_id)
            elif subtype in ['Staff', '2hStaff']: SHOPS['Shop_Rods'].append(item_id)
            elif subtype in ['Mace', '2hMace']: SHOPS['Shop_Maces'].append(item_id)
            elif subtype in ['Knuckle']: SHOPS['Shop_Knuckles'].append(item_id)
            elif subtype in ['Book']: SHOPS['Shop_Books'].append(item_id)
            elif subtype in ['Dagger']: SHOPS['Shop_Daggers'].append(item_id)
            elif subtype in ['1hSpear', '2hSpear']: SHOPS['Shop_Spears'].append(item_id)
            elif subtype in ['Katar']: SHOPS['Shop_Katars'].append(item_id)
            elif subtype in ['1hAxe', '2hAxe']: SHOPS['Shop_Axes'].append(item_id)
            elif subtype in ['Revolver', 'Rifle', 'Gatling', 'Shotgun', 'Grenade']: SHOPS['Shop_Guns'].append(item_id)
            elif subtype in ['Huuma']: SHOPS['Shop_Huuma'].append(item_id)

        # -- Armor / Head / Shield / Acc --
        elif type_ == 'Armor':
            # Check Locations
            if not locs: continue
            
            # Armor
            if locs.get('Armor'): SHOPS['Shop_Body'].append(item_id)
            if locs.get('Garment'): SHOPS['Shop_Robe'].append(item_id)
            if locs.get('Shoes'): SHOPS['Shop_Shoes'].append(item_id)
            if locs.get('Shield'): 
                SHOPS['Shop_Shields_A'].append(item_id)
                SHOPS['Shop_Shields_W'].append(item_id) # Add to Weapon shop too
            
            # Head
            if locs.get('Head_Top'): SHOPS['Shop_Head_Top'].append(item_id)
            elif locs.get('Head_Mid'): SHOPS['Shop_Head_Mid'].append(item_id)
            elif locs.get('Head_Low'): SHOPS['Shop_Head_Low'].append(item_id)
            
            # Accessory
            if locs.get('Accessory') or locs.get('Accessory_R') or locs.get('Accessory_L') or locs.get('Both_Accessory'):
                SHOPS['Shop_Accessories'].append(item_id)

        # -- Ammo --
        elif type_ == 'Ammo':
            if subtype == 'Arrow': SHOPS['Shop_Arrows'].append(item_id)
            elif subtype in ['Bullet', 'Shell', 'Cannonball']: SHOPS['Shop_Bullets'].append(item_id)
            elif subtype in ['Shuriken', 'Kunai', 'Knife']: SHOPS['Shop_Ninjas'].append(item_id) # Knife = Venom Knife?

        # -- Consumables --
        elif type_ in ['Healing', 'Usable', 'Cash']:
            # Heuristics
            n_lower = name.lower()
            if type_ == 'Healing':
                SHOPS['Shop_Health'].append(item_id)
            elif 'scroll' in n_lower:
                SHOPS['Shop_Scrolls'].append(item_id)
            elif 'converter' in n_lower or 'elemental' in n_lower:
                SHOPS['Shop_Enchant'].append(item_id)
            elif type_ == 'Usable' or type_ == 'Cash':
                # Exclude if already scroll/enchant
                # Assume Buff/Food
                # Filter out some garbage?
                SHOPS['Shop_Buffs'].append(item_id)

        # -- Cards --
        elif type_ == 'Card':
            if locs.get('Right_Hand'): SHOPS['Shop_Card_Weap'].append(item_id)
            elif locs.get('Shoes'): SHOPS['Shop_Card_Shoe'].append(item_id)
            elif locs.get('Garment'): SHOPS['Shop_Card_Garm'].append(item_id)
            elif locs.get('Accessory') or locs.get('Both_Accessory') or locs.get('Accessory_R') or locs.get('Accessory_L'): SHOPS['Shop_Card_Acc'].append(item_id)
            elif locs.get('Armor'): SHOPS['Shop_Card_Arm'].append(item_id)
            elif locs.get('Left_Hand'): SHOPS['Shop_Card_Shld'].append(item_id)
            elif locs.get('Head_Top') or locs.get('Head_Mid') or locs.get('Head_Low'): SHOPS['Shop_Card_Head'].append(item_id)

        # -- Etc / Crafting / Useful --
        elif type_ == 'Etc':
            n_lower = name.lower()
            # Crafting
            if 'anvil' in n_lower or 'hammer' in n_lower or 'iron' in n_lower or 'steel' in n_lower or 'ore' in n_lower or 'star dust' in n_lower:
                SHOPS['Shop_Forging'].append(item_id)
            elif 'herb' in n_lower or 'spore' in n_lower or 'stem' in n_lower or 'alcohol' in n_lower or 'bottle' in n_lower or 'solution' in n_lower or 'tube' in n_lower or 'karvodailnirol' in n_lower:
                SHOPS['Shop_Alchemy'].append(item_id)
            elif 'gemstone' in n_lower or 'pearl' in n_lower or 'diamond' in n_lower or 'opal' in n_lower or 'zircon' in n_lower:
                SHOPS['Shop_Gems'].append(item_id)
            elif 'wood' in n_lower or 'point' in n_lower or 'venom' in n_lower or 'rune' in n_lower:
                SHOPS['Shop_Craft_Class'].append(item_id)
            
            # Useful
            elif item_id in [714, 984, 985, 756, 757, 604, 523]: # Emperium, Oridecon, Elunium, etc. (IDs might be wrong, using keywords is better)
                pass # Handled below
            
            if 'emperium' in n_lower or 'elunium' in n_lower or 'oridecon' in n_lower or 'carnium' in n_lower or 'bradium' in n_lower or 'dead branch' in n_lower or 'bloody branch' in n_lower or 'gold' in n_lower:
                 SHOPS['Shop_Useful'].append(item_id)

def generate_script():
    print("Generating script...")
    
    # NPC Definitions
    # darkmall,x,y,dir script Name SpriteID,{
    
    script = """// Ravena Market Script
// Generated automatically
// Date: 2026-01-06

// -- NPCs --

// 1. Weapons (83, 108)
darkmall,83,108,4	script	Armas	404,{
	mes "[Armas]";
	mes "O que deseja?";
	menu 
		"Arcos", L_Bow,
		"Instrumentos", L_Inst,
		"Chicotes", L_Whip,
		"Espadas", L_1hSw,
		"Espadoes", L_2hSw,
		"Cajados", L_Rod,
		"Macas", L_Mace,
		"Luvas", L_Knuc,
		"Livros", L_Book,
		"Adagas", L_Dagg,
		"Lancas", L_Spea,
		"Katars", L_Kata,
		"Machados", L_Axe,
		"Pistolas", L_Gun,
		"Huuma", L_Huum,
		"Escudos", L_Shld,
		"Flechas", L_Arro,
		"Municoes", L_Bull,
		"Ninjas", L_Ninj;
		
L_Bow: close2; callshop "Shop_Bows",1; end;
L_Inst: close2; callshop "Shop_Instruments",1; end;
L_Whip: close2; callshop "Shop_Whips",1; end;
L_1hSw: close2; callshop "Shop_1hSwords",1; end;
L_2hSw: close2; callshop "Shop_2hSwords",1; end;
L_Rod: close2; callshop "Shop_Rods",1; end;
L_Mace: close2; callshop "Shop_Maces",1; end;
L_Knuc: close2; callshop "Shop_Knuckles",1; end;
L_Book: close2; callshop "Shop_Books",1; end;
L_Dagg: close2; callshop "Shop_Daggers",1; end;
L_Spea: close2; callshop "Shop_Spears",1; end;
L_Kata: close2; callshop "Shop_Katars",1; end;
L_Axe: close2; callshop "Shop_Axes",1; end;
L_Gun: close2; callshop "Shop_Guns",1; end;
L_Huum: close2; callshop "Shop_Huuma",1; end;
L_Shld: close2; callshop "Shop_Shields_W",1; end;
L_Arro: close2; callshop "Shop_Arrows",1; end;
L_Bull: close2; callshop "Shop_Bullets",1; end;
L_Ninj: close2; callshop "Shop_Ninjas",1; end;
}

// 2. Armor (83, 107)
darkmall,83,107,4	script	Armaduras	413,{
	mes "[Armaduras]";
	mes "Escolha:";
	menu
		"Vestimentas", L_Body,
		"Capas", L_Robe,
		"Calcados", L_Shoe,
		"Escudos", L_ShldA;

L_Body: close2; callshop "Shop_Body",1; end;
L_Robe: close2; callshop "Shop_Robe",1; end;
L_Shoe: close2; callshop "Shop_Shoes",1; end;
L_ShldA: close2; callshop "Shop_Shields_A",1; end;
}

// 3. Head (83, 88)
darkmall,83,88,4	script	Cabeca	405,{
	mes "[Cabeca]";
	mes "Escolha:";
	menu
		"Topo", L_Top,
		"Meio", L_Mid,
		"Baixo", L_Low;

L_Top: close2; callshop "Shop_Head_Top",1; end;
L_Mid: close2; callshop "Shop_Head_Mid",1; end;
L_Low: close2; callshop "Shop_Head_Low",1; end;
}

// 4. Accessories (83, 87)
darkmall,83,87,4	script	Acessorios	408,{
	mes "[Acessorios]";
	mes "Deseja ver acessorios?";
	menu
		"Ver Acessorios", L_Acc;

L_Acc: close2; callshop "Shop_Accessories",1; end;
}

// 5. Consumables (116, 108)
darkmall,116,108,4	script	Consumiveis	453,{
	mes "[Consumiveis]";
	mes "Escolha:";
	menu
		"Cura", L_Heal,
		"Buffs", L_Buff,
		"Pergaminhos", L_Scro,
		"Encantos", L_Ench;

L_Heal: close2; callshop "Shop_Health",1; end;
L_Buff: close2; callshop "Shop_Buffs",1; end;
L_Scro: close2; callshop "Shop_Scrolls",1; end;
L_Ench: close2; callshop "Shop_Enchant",1; end;
}

// 6. Cards (116, 107)
darkmall,116,107,4	script	Cartas	435,{
	mes "[Cartas]";
	mes "Escolha:";
	menu
		"Armas", L_CWeap,
		"Sapatos", L_CShoe,
		"Capas", L_CGarm,
		"Acessorios", L_CAcc,
		"Armaduras", L_CArm,
		"Escudos", L_CShld,
		"Cabeca", L_CHead;

L_CWeap: close2; callshop "Shop_Card_Weap",1; end;
L_CShoe: close2; callshop "Shop_Card_Shoe",1; end;
L_CGarm: close2; callshop "Shop_Card_Garm",1; end;
L_CAcc: close2; callshop "Shop_Card_Acc",1; end;
L_CArm: close2; callshop "Shop_Card_Arm",1; end;
L_CShld: close2; callshop "Shop_Card_Shld",1; end;
L_CHead: close2; callshop "Shop_Card_Head",1; end;
}

// 7. Crafting (116, 88)
darkmall,116,88,4	script	Artesanato	472,{
	mes "[Artesanato]";
	mes "Escolha:";
	menu
		"Forja", L_Forg,
		"Alquimia", L_Alch,
		"Gemas", L_Gems,
		"Classes", L_CrCl;

L_Forg: close2; callshop "Shop_Forging",1; end;
L_Alch: close2; callshop "Shop_Alchemy",1; end;
L_Gems: close2; callshop "Shop_Gems",1; end;
L_CrCl: close2; callshop "Shop_Craft_Class",1; end;
}

// 8. Useful (116, 87)
darkmall,116,87,4	script	Uteis	496,{
	mes "[Uteis]";
	mes "Itens Uteis e Raros.";
	menu
		"Ver Itens", L_Use;

L_Use: close2; callshop "Shop_Useful",1; end;
}

// -- Shops --
"""
    
    with open(OUTPUT_PATH, 'w', encoding='iso-8859-1') as f:
        f.write(script)
        
        for shop_name, items in SHOPS.items():
            if not items:
                # Add a dummy item if empty to avoid errors
                items = [501] # Red Potion
            
            # Remove duplicates and sort
            items = sorted(list(set(items)))
            
            # Split items into chunks if too many? 
            # rAthena 'shop' command has a limit on line length/items?
            # Max items per shop is usually defined in src/map/shop.hpp (MAX_SHOP_ITEMS).
            # Default is 100 or so? No, it's often higher now.
            # But string length in script might be an issue.
            # I will write as one line. If it fails, I'll know.
            # Format: -1,ID:100,ID:100,...
            
            item_str = ",".join([f"{id}:100" for id in items])
            
            f.write(f"\ndarkmall,1,1,0\tshop\t{shop_name}\t-1,{item_str}\n")
    
    print(f"Written to {OUTPUT_PATH}")

def main():
    # Load items
    items_equip = load_yaml('item_db_equip.yml')
    items_usable = load_yaml('item_db_usable.yml')
    items_etc = load_yaml('item_db_etc.yml')
    
    print("Processing Items...")
    process_items(items_equip)
    process_items(items_usable)
    process_items(items_etc)
    
    generate_script()

if __name__ == '__main__':
    main()
