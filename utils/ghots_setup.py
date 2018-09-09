# coding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from collections import namedtuple
import logging

from google.appengine.ext import ndb

from models.ghosts import Ghost

DefaultGhost = namedtuple('DefaultGhost', 'name, description')

GHOST_NAMES = (
    DefaultGhost('Betelgeuse', '(Beetlejuice): The Ghost with the Most.'),
    DefaultGhost('Bhoot', '(Indian folklore): The restless ghost of a deceased person, usually appearing in human form but with backward-facing feet. Bhoots tend to appear in white, often floating above the ground or in trees, and cast no shadow.'),
    DefaultGhost('Bloody Mary', '(American folklore): Other urban legends may come and go, but proud Mary keeps on burning. As long as there are sleepover parties, there will be someone bold enough to say her name three times in front of a mirror at midnight. We should totally hook her up with Betelgeuse. Or the Candyman.'),
    DefaultGhost('Bogle', '(Scottish/English folklore): Goblin-esque ghostly beings who delight in messing with humans, usually to annoy, perplex, or simply frighten (rather than inflicting serious harm). For example, “Tatty Bogle” would hide in potato fields and cause blight, when not attacking unsuspecting humans. Hilarious!'),
    DefaultGhost('Casper', '(Scottish/English folklore): Goblin-esque ghostly beings who delight in messing with humans, usually to annoy, perplex, or simply frighten (rather than inflicting serious harm). For example, “Tatty Bogle” would hide in potato fields and cause blight, when not attacking unsuspecting humans. Hilarious!'),
    DefaultGhost('Chindi', '(Navajo folklore): The ghost that leaves the body with a person’s last breath, containing everything that was bad or unharmonious in their spirit. After death, the dead person’s name is never spoken and their remains and possessions are avoided in order to avoid chindi-inflicted “ghost sickness.”'),
    DefaultGhost('Cihuateteo', '(Aztec mythology): The ancient Aztecs regarded childbirth as a form of battle, so women who died giving birth were honored as fallen warriors. In death, they became the fearsome Cihuateteo, known for haunting crossroads, causing sickness and madness, and stealing children. Do not get on their bad side.'),
    DefaultGhost('Clytemnestra', '(Greek myth/drama): One of the first ghosts to appear in a work of fiction, Aeschylus’s Oresteia (458 BC) portrays her as a scheming femme fatale who murders her husband and is in turn killed by her son, Orestes. Her vengeful spirit appears to spur The Furies to action, urging them to torment and punish Orestes. Even in death, she’s not a woman to be trifled with...'),
    DefaultGhost('Draugr', '(Norse mythology): Undead Vikings who possess superhuman strength, the ability to swell and increase their size or shapeshift at will, and reek of decay. They delight in violently slaughtering and sometimes consuming their victims, usually people who have trespassed on the graves or burial mounds the draugr guards, although sometimes they roam and rampage, killing animals and humans alike.'),
    DefaultGhost('Dybbuk', '(Jewish Folklore): Malevolent spirit believed to be the soul of a dead person, able to possess the living. Contrast with Ibbur.'),
    DefaultGhost('Gjenganger', '(Scandinavian folklore): The ghost of a dead person (often murderers, murder victims, or suicides) who, though undead, took on corporeal form and threatened the living with violence or torment. They could also administer the dødningeknip (or “dead man’s pinch), which would cause disease and death to befall the victim.'),
    DefaultGhost('Guĭ', '(Chinese folklore): The general Chinese term for ghosts, there are many different types and categorizations of Guĭ; Yuān Guǐ, for example, is the term for a ghost who has died a wrongful death, Wú Tóu Guǐ is a wandering headless specter, and Shuǐ Guǐ are ghosts of the drowned, who attack the living and drag them under water, hoping to drown their victims and take possession of their body. The spirits of the dead are celebrated in Chinese culture are celebrated in an annual ghost festival, when the realms of the living and the realms of Heaven and Hell are open, allowing the dead to interact with the living, and particularly their family and descendants.'),
    DefaultGhost('Ibbur', '(Jewish Folklore): Unlike the dybbuk, a positive form of possession in which a benevolent soul temporarily inhabits a living person in a beneficial and positive way.'),
    DefaultGhost('Jima', '(Amazonian folklore): Feared by the Wari, an Amazonian rainforest tribe, Jima are terrifying specters known for grabbing their living victims with their incredibly strong, cold, poisonous hands and attempting to tear the victim’s spirit away.'),
    DefaultGhost('Jinn', '(Quran/Islamic mythology): Jinn (also known as djinn or genies), are described in the Quran as spirits made of smokeless, scorching fire, and can be evil, good, or neutral in their interactions with humans.'),
    DefaultGhost('La Llorona', '(Spanish/Mexican legend): The Weeping Woman, a spirit who drowned her children in order to be with her lover, but was rejected and committed suicide. Constantly crying, La Llorona is doomed to eternally search for her children in vain, sometimes attempting to steal living children who wander or misbehave.'),
    DefaultGhost('Moaning Myrtle', '(Harry Potter): Muggle-born witch, killed by a Basilisk when she caught Tom Riddle opening the Chamber of Secrets. Her ghost haunts the Hogwarts bathroom in which she died (occasionally branching out to other bathrooms in the castle). Myrtle sometimes helps Harry, when she’s not crying or desperately flirting with him.'),
    DefaultGhost('Mr. Boogedy', '(Mr. Boogedy): The star of a surprisingly unsettling late-80s Disney movie, Mr. Boogedy is the ghost of cranky pilgrim who sold his soul to Satan for a magic cloak, and ends up haunting David Faustino and Kristy Swanson, for some reason.'),
    DefaultGhost('Nachzehrer', '(German folklore): Supernatural being similar to a vampire, often tied to suicide or accidental death. The nachzehrer awakes after death and often attempts to devour its living family members, but sometimes consumes its own flesh in the grave. Powers include causing death by casting a shadow on the living, or by ringing church bells, killing everyone within hearing.'),
    DefaultGhost('Blinky', '(Video game): Pac-Man’s nemeses, each ghost has a nickname and is associated with a particular character trait within the game. “Blinky” (red) shadows Pac-Man, chasing him; “Pinky” (pink) is speedy; “Inky” (blue) is bashful, and “Clyde” (orange) is pokey, slower and more random in his movements. This developed out of the original Japanese version, Puck-Man, in which the ghosts’ personalities can be translated as Chaser, Ambusher, Fickle, and Stupid, respectively.'),
    DefaultGhost('Pinky', ''),
    DefaultGhost('Inky', ''),
    DefaultGhost('Clyde', ''),
    DefaultGhost('Patrick Swayze', '(Ghost): The sexiest ghost of all. Good with clay and Whoopi Goldberg.'),
    DefaultGhost('Phi Tai Hong', '(Thai folkore): The most feared type of ghost in all of Thai folklore, a restless and angry spirit of a person who suffered a violent death.'),
    DefaultGhost('Pishacha', '(Hindu mythology): Demonic ghosts that feed on flesh and human energies, capable of possessing humans and altering their thoughts, sometimes leading to madness. Like bhuts, pishacha are often depicted as haunting cremation grounds.'),
    DefaultGhost('Poltergeist', '(Various folklores): While the common term for this comes from the German words for “noisy ghost,” poltergeists feature in the folklore of many cultures. The term usually denotes a disruptive entity that haunts a particular person via strange noises and even petty physical attacks. Poltergeist activity is a popular subject in TV in movies, featuring in everything from Blithe Spirit to Harry Potter to the Poltergeist movies.'),
    DefaultGhost('Revenant', '(European folklore): General term for an undead corpse or visible ghost that returns from the grave, usually for malevolent purposes. Stories involving revenants usually depict a specific undead person who returns with a purpose, such as revenge against a killer or those responsible for their death, or to harass people who wronged them during life.'),
    DefaultGhost('Ringwraith', '(Lord of the Rings): Not technically ghosts, perhaps, but certainly spooky enough to make the list, the Ringwraiths (also known as Nazgûl or Black Riders) began as nine mortal men to whom Sauron gave Rings of Power. The rings gave them power and extended their lives, but it also corrupted and destroyed them, turning them into undead thralls even after their corporeal form faded away.'),
    DefaultGhost('Slender Man', '(Internet myth): No one knows what the Slender Man is; his defining characteristic is mystery, with the ability to inspire fear a close second. An urban legend for the 21st century, the Slender Man stalks his victims, sometimes over long periods of time, and may inspire amnesia, paranoia, and madness; he is allegedly responsible for various unexplained disappearances. All we really know is, the Slender Man is terrifying.'),
    DefaultGhost('Slimer', '(Ghostbusters): Made of pure ectoplasm, Slimer is classified as a focused, non-terminal repeating phantasm, or a Class 5 full roaming vapor (and a real nasty one, at that). After the Ghostbusters stop him from haunting the Sedgewick Hotel, he became kind of a pet and a mascot, and became a more developed character in the Animated Series. Dan Ackroyd has referred to Slimer as ”The Ghost of John Belushi."'),
    DefaultGhost('Space Ghost', '(Space Ghost and Dino Boy/Space Ghost Coast to Coast): One of the greatest talk show hosts of all time, often accompanied by his nemeses/sidekicks Zorak, Moltar and Brak. Designed by the great Alex Toth, Space Ghost started out as superhero who fought villains and faced off against The Council of Doom (in space. Natch.), before signing on to host his own show on the Cartoon Network.'),
    DefaultGhost('Strigoi', '(Romanian folklore): Troubled souls risen from the grave, a tradition dating back through Indo-European Dacian/Thracian mythology. Strigoi are often seen as being similar to vampires, immortal undead, but also manifest as evil spirits who haunt the living, often their living family members.'),
    DefaultGhost('Candyman', '(Candyman): In life, the Candyman was the son of a slave who became a well-known artist; when he fell in love with a white woman, an angry mob cut off his hand, replacing it with a hook, smeared him with honey, and watched as he was stung to death by bees. According to the film’s urban legend, he can be summoned by saying his name five times in a mirror, but since we’re talking about Tony Todd with a hook-hand, it’s not recommended.'),
    DefaultGhost('The Crypt Keeper', '(Tales from the Crypt): In the 50s, the Crypt Keeper started out as the narrator of EC’s horror comic anthology series Tales from the Crypt, until the Comics Code quickly brought about its untimely death. In 1989, however, the character was revived as a cackling animated corpse in order to host the HBO series of the same name. With lines like, “Hello, boils and ghouls!”, the Crypt Keeper’s moldering puns were usually the most deadly part of the show.'),
    DefaultGhost('Headless Horseman', '(“The Legend of Sleepy Hollow”): In Irving’s classic short story, the Horseman is the ghost of a Hessian soldier decapitated by a cannonball during the American Revolution. While it is suggested in the story that the “spirit” who chases schoolteacher Ichabod Crane might really be Crane’s romantic rival impersonating the ghost to scare him off, the legend of the Headless Horseman remains potent (and if you haven’t seen the Disney adaptation or Christopher Walken’s take on the character in Sleepy Hollow, then you are missing out).'),
    DefaultGhost('Tomás', '(El Orfanato/The Orphanage): The protagonist of Spanish suspense/horror film The Orphanage first encounters Tomás as the imaginary friend of her adopted son, Simón—but as events turn sinister, he becomes more of a definite, if ghostly, presence. Depicted through most of the film as a small boy wearing a disturbing mask stitched together out of sackcloth, Tomás is simultaneously horrifying and heartbreaking.'),
    DefaultGhost('Vetala', '(Hindu folklore): Spirits who tend to haunt places of burial and charnel grounds; trapped between life and the afterlife, they can take possession of corpses and cause all kinds of crazy trouble for the living.'),
    DefaultGhost('Wiedergänger', '(German folklore): Category of undead spirits who would trouble or torment the living in different ways; some types would jump on the backs of their victims and grow heavier and heavier until they broke down, exhausted or dead. Another variation is the headless rider, which made its way from European ghost story to American literature thanks to Washington Irving.'),
    DefaultGhost('Xunantunich', '(Real life/Archaeology): The name of this ancient Mayan archaeological site in Belize comes from Mayan words for “Stone Woman,” after the ghostly figure who has been seen haunting the site since 1892. Dressed all in white with fiery, red glowing eyes, the woman reportedly appears at the site, ascends the steps of the ceremonial pyramid and disappears into a stone wall.'),
    DefaultGhost('Yūrei', '(Japanese folklore): Used as a general term; there are also more specific types of ghosts, like the Onryō (vengeful spirits who return from purgatory), Goryō (aristocratic ghosts, often vengeful martyrs), or Zashiki-warashi (mischievous ghost children).'),
    DefaultGhost('Zhong Kui', '(Chinese mythology): By some accounts, Zhong Kui is the ghost (Guĭ) of a man who failed his civil service exams and committed suicide, he is a vanquisher of ghosts and evil spirits: a ghost who hunts other ghosts.'),
    DefaultGhost('Zuul', '(Ghostbusters): The Gatekeeper of Gozer; minion of The Destructor. Lovely singing voice, but with an unfortunate tendency to manifest as a Terror Dog and/or take over your fridge.'),
)


def ghost_initial_set_up():
    """
    Runs on deploy.
    Populates datastore with the default set of ghosts if none exists.
    """
    available_ghosts = Ghost.query().fetch(keys_only=True, limit=10)
    if len(available_ghosts) == 0:
        logging.info('No ghosts available. Adding new ghosts...')
        ghost_to_add = []
        for new_ghost in GHOST_NAMES:
            logging.info('Adding %s to datastore' % new_ghost.name)
            ghost_to_add.append(Ghost(name=new_ghost.name,
                                      description=new_ghost.description))
        ndb.put_multi(ghost_to_add)
