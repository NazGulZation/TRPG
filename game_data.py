class GameData:
    def __init__(self):
        self.scenes = {}
        self.stat_changes = {}
        self.items_gained = {}
        self._build_scenes()
        self._build_stat_changes()
        self._build_items_gained()
    
    def _build_scenes(self):
        self.scenes = {}
        self._add_prologue_start()
        self._add_village_panic()
        self._add_dark_prayer()
        self._add_search_chamber()
        self._add_confession()
        self._add_false_promise()
        self._add_walk_into_dark()
        self._add_frozen_despair()
        self._add_follow_trail()
        self._add_quest_accepted()
        self._add_refuse_quest()
        self._add_chapter_one_start()
        self._add_restart()
    
    def _add_prologue_start(self):
        self.scenes['prologue_start'] = {
            'title': 'The Dying Light',
            'text': (
                "The ember flickers.\n\n"
                "You have watched it for thirty years — this fragile sphere of amber light "
                "that keeps the village of Duskhollow alive. It has never faltered. Not through "
                "the Long Storms. Not through the Frozen Years. Not once in all your service as "
                "Warden of the Flame.\n\n"
                "Until tonight.\n\n"
                "A crack splits the air. The ember dims, and the warmth drains from the chamber "
                "like blood from a wound. You reach for it, but your hands — your damned, "
                "trembling hands — are too slow.\n\n"
                "The light dies.\n\n"
                "In the darkness that follows, you hear the first scream rise from the village below."
            ),
            'choices': [
                {'text': 'Rush to the village — they need you now', 'next': 'village_panic'},
                {'text': 'Kneel in the darkness and pray to forgotten gods', 'next': 'dark_prayer'},
                {'text': 'Search the chamber for answers — this should not have happened', 'next': 'search_chamber'}
            ],
            'atmosphere': 'dark'
        }
    
    def _add_village_panic(self):
        self.scenes['village_panic'] = {
            'title': 'The Cold Descends',
            'text': (
                "You descend the spiral stairs three at a time, your cloak billowing behind you. "
                "The cold is already seeping through the stone — a creeping, hungry thing that "
                "clings to your bones.\n\n"
                "The village square is chaos.\n\n"
                "Families huddle around dead hearths. Mothers clutch children who have already "
                "begun to shiver. Old Maren, the baker, stands in the center of the square, "
                "staring at the blackened spire where the ember once burned.\n\n"
                '"Warden," she whispers when she sees you. Her eyes are hollow. "What have you done?"\n\n'
                "The question cuts deeper than the cold. You open your mouth to answer, but "
                "the words die in your throat. Because you know — you have always known — "
                "that you were not at your post when the ember failed.\n\n"
                "You were in the tavern. Drinking. Forgetting.\n\n"
                "For the first time in thirty years, you had looked away."
            ),
            'choices': [
                {'text': 'Confess your failure to the village', 'next': 'confession'},
                {'text': 'Promise to find a new flame — lie to give them hope', 'next': 'false_promise'},
                {'text': 'Say nothing. Turn and walk into the frozen dark alone', 'next': 'walk_into_dark'}
            ],
            'atmosphere': 'cold'
        }
    
    def _add_dark_prayer(self):
        self.scenes['dark_prayer'] = {
            'title': 'Words to the Void',
            'text': (
                "You fall to your knees on the cold stone floor. The darkness is absolute — "
                "not the gentle dark of night, but the suffocating black of a world that has "
                "forgotten the sun.\n\n"
                '"Please," you whisper. The word feels pathetic. "Please, not them. Not the children. '
                "Take me instead. Take whatever you want. Just... let there be warmth again.\"\n\n"
                "Silence.\n\n"
                "Then — a sound. Not an answer. A memory.\n\n"
                "You see yourself, thirty years ago, standing before the Council of Wardens. "
                "Young. Certain. Swearing the oath: *I am the flame's keeper. I am the last "
                "light against the dark. I will not falter.*\n\n"
                "You were so sure you meant it.\n\n"
                "The memory shifts. You see the tavern. The amber liquid. The warm laughter "
                "of strangers who did not know what you had abandoned. You see yourself "
                "raising a glass while the ember died alone.\n\n"
                "When you open your eyes, tears have frozen on your cheeks."
            ),
            'atmosphere': 'dark'
        }
    
    def _add_search_chamber(self):
        self.scenes['search_chamber'] = {
            'title': "The Warden's Secret",
            'text': (
                "Your hands shake as you search the chamber. The ember's pedestal is cold — "
                "impossibly cold, as if it has been dead for years rather than moments.\n\n"
                "This is wrong. Embers do not simply die. They are eternal. That is what "
                "the Council taught. That is what you have given your life to protect.\n\n"
                "Your fingers find something at the base of the pedestal. A mark. Carved "
                "fresh into the stone.\n\n"
                "A single word: **COME**.\n\n"
                "Beneath it, a symbol you have not seen since your training — the sigil of "
                "the Hollow King. A myth. A story told to frighten young Wardens. A warning "
                "that the darkness was not empty. That something waited. That something *hungered*.\n\n"
                "The mark is still warm.\n\n"
                "Whatever did this... was here. Recently. Perhaps still is.\n\n"
                "From below, the screaming grows louder."
            ),
            'choices': [
                {'text': 'Take the sigil as evidence and go to the village', 'next': 'village_panic'},
                {'text': 'Follow the trail — find what did this', 'next': 'follow_trail'}
            ],
            'atmosphere': 'ominous'
        }
    
    def _add_confession(self):
        self.scenes['confession'] = {
            'title': 'The Weight of Truth',
            'text': (
                "You stand before them — these people who trusted you, who gave you purpose, "
                "who called you Warden as if the title meant something sacred.\n\n"
                '"I was not at my post," you say. Your voice cracks. "I left the ember '
                'unattended. I was... I was drinking. In the tavern. While it died."\n\n'
                "The silence that follows is worse than any scream.\n\n"
                "Old Maren steps forward. You expect rage. You expect stones. Instead, she "
                "places a withered hand on your arm.\n\n"
                '"Then you will fix it," she says simply. "That is what Wardens do."\n\n'
                "But her eyes betray her. She does not believe you can. And neither do you.\n\n"
                "A young woman pushes through the crowd — Elara, the scholar's daughter. "
                '"There are stories," she says, her voice barely audible. "Old stories. '
                'Of a place beyond the Frozen Reach where the last true fire still burns. '
                'The Emberheart."\n\n'
                "She pauses.\n\n"
                '"But no one who has sought it has ever returned."'
            ),
            'choices': [
                {'text': 'Sworn to find the Emberheart — accept the quest', 'next': 'quest_accepted'},
                {'text': 'Refuse — send no one else to die for your failure', 'next': 'refuse_quest'}
            ],
            'atmosphere': 'somber'
        }
    
    def _add_false_promise(self):
        self.scenes['false_promise'] = {
            'title': 'The Lie That Burns',
            'text': (
                '"The ember can be relit," you declare, and the lie tastes like ash on your tongue.\n\n'
                "The crowd surges forward. Hope — desperate, fragile, dangerous hope — "
                "flickers in their eyes like a candle in a storm.\n\n"
                '"How?" someone demands. "How long do we have?"\n\n'
                "You do not know. You are making this up as you speak, weaving a fiction "
                "from desperation and guilt.\n\n"
                '"Three days," you say. "Perhaps four. I need to... consult the old texts. '
                'There is a ritual. It requires... components. From beyond the village."\n\n'
                "They believe you. Gods help them, they believe you.\n\n"
                "Only Elara, the scholar's daughter, watches you with knowing eyes. "
                "She says nothing. But when the crowd disperses to spread the news, "
                "she catches your arm.\n\n"
                '"There is no ritual," she whispers. "Is there?"\n\n'
                "You cannot meet her gaze."
            ),
            'choices': [
                {'text': 'Admit the truth to Elara alone', 'next': 'confession'},
                {'text': 'Double down — you will find a way, even if it kills you', 'next': 'quest_accepted'}
            ],
            'atmosphere': 'tense'
        }
    
    def _add_walk_into_dark(self):
        self.scenes['walk_into_dark'] = {
            'title': 'The Frozen Dark',
            'text': (
                "You turn your back on the village. On the people. On everything.\n\n"
                "The cold hits you like a wall the moment you step beyond the village boundary. "
                "It is not merely the absence of warmth — it is a presence. A living thing "
                "that wraps around you and squeezes.\n\n"
                "You walk.\n\n"
                "The snow swallows your footprints within moments. The wind erases your "
                "footsteps from memory. You are being unmade, slowly, by the dark.\n\n"
                "Hours pass. Or days. Time has no meaning here.\n\n"
                "Then you see it — a figure, standing alone in the white expanse. "
                "It does not move. It does not breathe. It simply waits.\n\n"
                "As you draw closer, you see its face.\n\n"
                "It is your face.\n\n"
                'The figure speaks with your voice: "You cannot outrun what you are."'
            ),
            'atmosphere': 'dark'
        }
    
    def _add_frozen_despair(self):
        self.scenes['frozen_despair'] = {
            'title': 'The End of All Warmth',
            'text': (
                "You stop walking.\n\n"
                "The cold has seeped so deep into your bones that you can no longer feel "
                "your fingers. Your toes. Your face. You are becoming part of the frozen "
                "landscape — another statue in the white waste.\n\n"
                "Perhaps this is what you deserve.\n\n"
                "You think of the children in the village. Their laughter. Their warmth. "
                "The way they used to gather around the spire on festival nights, faces "
                "upturned to the ember's golden light.\n\n"
                "You took that from them.\n\n"
                "The snow begins to cover you. It is almost gentle. Almost kind.\n\n"
                "But then — a hand. Grabbing your collar. Pulling you back.\n\n"
                "Elara. Her face is blue with cold, her eyes fierce with determination.\n\n"
                '"You do not get to die," she hisses through chattering teeth. "Not yet. '
                'Not until you fix what you broke."\n\n'
                "She drags you back toward the village. And for the first time since the ember died, "
                "you feel something other than cold.\n\n"
                "Shame. And beneath it — faint, fragile — the smallest spark of purpose."
            ),
            'choices': [
                {'text': 'Let her lead you back — accept her faith in you', 'next': 'quest_accepted'}
            ],
            'atmosphere': 'cold'
        }
    
    def _add_follow_trail(self):
        self.scenes['follow_trail'] = {
            'title': 'Into the Deep',
            'text': (
                "The trail leads down. Below the chamber. Below the village. Into tunnels "
                "that should not exist — tunnels that predate the ember, predate the village, "
                "predate everything you have ever known.\n\n"
                "The walls are carved with scenes. You trace them with trembling fingers:\n\n"
                "A sun, dying. People, screaming. And beneath them all — a throne. "
                "And on the throne — a crown of black ice.\n\n"
                "The Hollow King.\n\n"
                "The stories were true. All of them. The darkness was not empty. It was "
                "ruled. And its king had been waiting — patient, eternal, hungry — for "
                "the last light to fail.\n\n"
                "You find a chamber. In its center, a pedestal. And on the pedestal — "
                "a book. Bound in something you do not want to identify.\n\n"
                "The pages fall open to a single passage:\n\n"
                '*"The ember was never eternal. It was borrowed. Stolen from the dark '
                'by those who came before. And the dark always collects its debts."*\n\n'
                "You understand now. The ember did not fail. It was *taken*.\n\n"
                "And the debt is due."
            ),
            'choices': [
                {'text': 'Take the book and return to the village', 'next': 'quest_accepted'},
                {'text': 'Continue deeper — confront the Hollow King', 'next': 'quest_accepted'}
            ],
            'atmosphere': 'ominous'
        }
    
    def _add_quest_accepted(self):
        self.scenes['quest_accepted'] = {
            'title': 'The Road Ahead',
            'text': (
                "Dawn does not come. It has not come in three hundred years. But the "
                "sky lightens to a deep, bruised purple — the closest thing to morning "
                "this world has known.\n\n"
                "You stand at the village gate. Behind you, Duskhollow — dying, cold, "
                "but still standing. Before you, the Frozen Reach — a wasteland of ice "
                "and shadow where no light has touched since the sun died.\n\n"
                "Elara stands beside you. She has insisted on coming. You could not "
                "dissuade her. Perhaps you did not try hard enough.\n\n"
                '"The Emberheart," she says, clutching her father\'s old maps. '
                '"If the stories are true, it lies beyond the Shattered Peaks. '
                'A week\'s journey. Perhaps more."\n\n'
                "She does not say what you both know: that no one who has attempted "
                "this journey has ever returned.\n\n"
                "You look back one last time. The blackened spire. The huddled figures. "
                "Old Maren, watching from her doorway.\n\n"
                "You failed them once. You will not fail them again.\n\n"
                "Even if the dark takes you. Even if the cold claims you. Even if "
                "the Hollow King himself stands between you and the flame.\n\n"
                "You step forward. Into the white. Into the silence.\n\n"
                "Into the story that will either save you... or end you.\n\n"
                "---\n\n"
                "**PROLOGUE COMPLETE**\n\n"
                "Your journey begins."
            ),
            'choices': [
                {'text': 'Begin your journey — the Frozen Reach awaits', 'next': 'chapter_one_start'},
                {'text': 'Return to the title screen', 'next': 'restart'}
            ],
            'atmosphere': 'hopeful'
        }
    
    def _add_refuse_quest(self):
        self.scenes['refuse_quest'] = {
            'title': "The Warden's Refusal",
            'text': (
                '"No," you say. The word falls like a stone. "I will not lead anyone else '
                'to die for my mistake."\n\n'
                "The crowd murmurs. Elara steps forward, her face pale with anger.\n\n"
                '"Then what?" she demands. "We simply wait here to freeze? You would '
                'let us all die because you are afraid?"\n\n'
                '"I am not afraid," you lie.\n\n'
                '"You are terrified," she says. "I can see it. But fear is not a reason '
                'to stop. It is a reason to be careful. To be smart. To *try*."\n\n'
                "She holds out her hand.\n\n"
                '"My father spent his life studying the old ways. He believed the '
                'Emberheart was real. He died believing it. Do not let his death — '
                'and yours — be for nothing."\n\n'
                "You look at her hand. Young. Steady. Unafraid.\n\n"
                "You think of the ember. Of the light. Of the warmth you took for granted.\n\n"
                "Perhaps... perhaps there is still a chance."
            ),
            'choices': [
                {'text': 'Take her hand — accept the quest together', 'next': 'quest_accepted'}
            ],
            'atmosphere': 'somber'
        }
    
    def _add_chapter_one_start(self):
        self.scenes['chapter_one_start'] = {
            'title': 'Chapter One: The Frozen Reach',
            'text': (
                "The wind howls across the white expanse like a dying animal.\n\n"
                "You and Elara walk in silence, each step a battle against the cold. "
                "The village has long since vanished behind you — swallowed by the "
                "endless snow.\n\n"
                "Ahead, the Shattered Peaks rise like broken teeth against the sky.\n\n"
                "Somewhere beyond them, if the stories are true, the Emberheart waits.\n\n"
                "But the dark between here and there is vast. And hungry.\n\n"
                "---\n\n"
                "*Chapter One continues in the full game...*\n\n"
                "*Thank you for playing the prologue of THE LAST EMBER.*"
            ),
            'choices': [
                {'text': 'Play again — make different choices', 'next': 'restart'}
            ],
            'atmosphere': 'cold'
        }
    
    def _add_restart(self):
        self.scenes['restart'] = {
            'title': 'The Last Ember',
            'text': (
                "The ember flickers.\n\n"
                "Would you watch it again?"
            ),
            'choices': [
                {'text': 'Begin again', 'next': 'prologue_start'}
            ],
            'atmosphere': 'dark'
        }

    def _build_stat_changes(self):
        self.stat_changes = {
            'prologue_start': {
                0: {'resolve': 10, 'guilt': 5},
                1: {'guilt': 15, 'hope': -5},
                2: {'resolve': 5, 'hope': 5}
            },
            'village_panic': {
                0: {'guilt': 10, 'resolve': 10},
                1: {'guilt': 15, 'hope': 10},
                2: {'guilt': 20, 'resolve': -5}
            },
            'dark_prayer': {
                0: {'resolve': 10},
                1: {'guilt': 20, 'hope': -10}
            },
            'search_chamber': {
                0: {'resolve': 5, 'hope': 5},
                1: {'resolve': 15, 'guilt': 5}
            },
            'confession': {
                0: {'resolve': 15, 'hope': 10},
                1: {'guilt': 15, 'resolve': -5}
            },
            'false_promise': {
                0: {'guilt': 5, 'resolve': 10},
                1: {'resolve': 15, 'guilt': 10}
            },
            'walk_into_dark': {
                0: {'guilt': 25, 'hope': -15},
                1: {'resolve': 15, 'guilt': 5}
            },
            'frozen_despair': {
                0: {'hope': 10, 'resolve': 10}
            },
            'follow_trail': {
                0: {'resolve': 10, 'hope': 5},
                1: {'resolve': 15, 'guilt': 5}
            },
            'quest_accepted': {
                0: {'resolve': 10, 'hope': 10},
                1: {}
            },
            'refuse_quest': {
                0: {'resolve': 15, 'hope': 10}
            },
            'chapter_one_start': {
                0: {}
            },
            'restart': {
                0: {}
            }
        }

    def _build_items_gained(self):
        self.items_gained = {
            'search_chamber': {
                0: ['Hollow King Sigil'],
                1: ['Hollow King Sigil']
            },
            'follow_trail': {
                0: ['The Dark Ledger'],
                1: ['The Dark Ledger']
            }
        }

    def get_scene(self, scene_id):
        return self.scenes.get(scene_id)

    def get_next_scene(self, current_scene_id, choice_index):
        scene = self.scenes.get(current_scene_id)
        if scene and choice_index < len(scene['choices']):
            return scene['choices'][choice_index]['next']
        return current_scene_id

    def get_stat_changes(self, scene_id, choice_index):
        scene_changes = self.stat_changes.get(scene_id, {})
        return scene_changes.get(choice_index, {})

    def get_items_gained(self, scene_id, choice_index):
        scene_items = self.items_gained.get(scene_id, {})
        return scene_items.get(choice_index, [])