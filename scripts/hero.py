"""Header: an illustrated, character-driven comedic SVG animation for GitHub's README.

Four illustrated characters share one dark obsidian workshop stage:
- Nitish (left, coffee in hand) watching his creations cause chaos
- Sparky (amber hard-hat power buddy) holding the live power cord
- Chip-Bot (cyan/emerald silicon & robotics buddy) caught in the middle
- Nimbus (floaty violet cloud buddy) who accidentally drops a hot spark on Chip-Bot
  and immediately whistles innocently while everyone points fingers.

Pure CSS @keyframes so it plays smoothly inside GitHub's <img> sandbox with
zero JavaScript, zero external fonts, and zero generic dashboard chrome.
"""

from svgkit import (ACCENT, ACCENT_2, ACCENT_MID, BG, GREEN, MUTED, SANS, SILICON, TEXT, VIOLET, WHITE, doc, esc, f)

W, H = 1200, 436
FLOOR_Y = 356
CYCLE = 13.0
PHASE = -5.4  # lands right in the peak 4-character comic standoff at t=0

# Character palette (drawn from portfolio obsidian + accents + Nitish's figure.js skin/hair)
SKIN = "#A96F51"
SKIN_DK = "#86533B"
SKIN_LT = "#BF8766"
HAIR = "#15100E"
HAIR_HI = "#362822"
SPARKY_SKIN = "#E8B896"
SPARKY_SHADE = "#C99572"
RED = "#FF5C5C"
BLUSH = "#FF7E9D"
BUBBLE_BG = "#161B26"
BUBBLE_STROKE = "#2B3347"


def pct(sec):
    return f"{f(sec / CYCLE * 100)}%"


def kf(name, stops):
    body = "".join(f"{pct(s)}{{{props}}}" for s, props in stops)
    return f"@keyframes {name}{{{body}}}"


def anim(name, easing="ease-in-out"):
    return f"animation:{name} {f(CYCLE)}s {easing} {f(PHASE)}s infinite"


def bubble(cx, cy, w, text_str, tail_dx=0, cls="", accent=BUBBLE_STROKE):
    """Clean, friendly comic speech bubble in natural sentence case."""
    x0 = -w / 2
    tx = tail_dx
    return f"""
<g transform="translate({f(cx)} {f(cy)})">
  <g class="{cls}">
    <rect x="{f(x0)}" y="-19" width="{w}" height="36" rx="18" fill="{BUBBLE_BG}" stroke="{accent}" stroke-width="1.5"/>
    <path d="M{f(tx - 6)} 16.5 L{f(tx)} 26 L{f(tx + 7)} 16.5 Z" fill="{BUBBLE_BG}" stroke="{accent}" stroke-width="1.5" stroke-linejoin="round"/>
    <line x1="{f(tx - 5)}" y1="16.5" x2="{f(tx + 6)}" y2="16.5" stroke="{BUBBLE_BG}" stroke-width="2.6"/>
    <text x="0" y="4" text-anchor="middle" font-family="{SANS}" font-size="14.5" font-weight="600" fill="{TEXT}">{esc(text_str)}</text>
  </g>
</g>"""


def nitish_character():
    """Illustrated Nitish character on the left: wavy hair, hoodie, coffee mug, interactive fix walk."""
    return f"""
<g transform="translate(178 {FLOOR_Y})">
  <g class="nitish-walk">
    <!-- Ground contact shadow -->
    <ellipse cx="0" cy="4" rx="46" ry="9" fill="#000" opacity=".48"/>
    <!-- Legs & sneakers -->
    <rect x="-22" y="-58" width="17" height="50" rx="8" fill="#181D2B"/>
    <rect x="6" y="-58" width="17" height="50" rx="8" fill="#181D2B"/>
    <path d="M-24 -10h22c4 0 6 3 6 7v4h-30v-5c0-3 1-6 2-6z" fill="#2A3244"/>
    <path d="M4 -10h24c4 0 6 3 6 7v4h-30v-11z" fill="#2A3244"/>
    <line x1="-24" y1="0" x2="2" y2="0" stroke="#E5E9F2" stroke-width="2.6" stroke-linecap="round"/>
    <line x1="4" y1="0" x2="32" y2="0" stroke="#E5E9F2" stroke-width="2.6" stroke-linecap="round"/>

    <!-- Breathing upper body -->
    <g class="nitish-bob">
      <!-- Left arm holding steaming coffee mug -->
      <g class="nitish-mug-arm" transform="translate(-31 -118)">
        <path d="M0 0 C-18 10 -24 30 -16 48" fill="none" stroke="#1E2536" stroke-width="16" stroke-linecap="round"/>
        <circle cx="-16" cy="50" r="8.5" fill="{SKIN}"/>
        <!-- Coffee mug -->
        <g transform="translate(-34 36)">
          <path d="M16 5c6 0 7 11 0 11" fill="none" stroke="#E8EDF7" stroke-width="2.6" stroke-linecap="round"/>
          <rect x="0" y="0" width="18" height="22" rx="4" fill="#EFF3FA"/>
          <rect x="0" y="8" width="18" height="5" fill="{ACCENT}"/>
          <!-- Gentle rising steam -->
          <path class="steam" d="M5 -4c-2 -5 3 -8 1 -13M12 -5c-2 -5 3 -8 1 -13" fill="none" stroke="{WHITE}" stroke-width="1.6" stroke-linecap="round" opacity=".45"/>
        </g>
      </g>

      <!-- Torso (charcoal hoodie over cream tee) -->
      <path d="M-34 -126 C-34 -138 -20 -144 0 -144 C20 -144 34 -138 34 -126 L30 -54 C30 -48 24 -45 18 -45 L-18 -45 C-24 -45 -30 -48 -30 -54 Z"
            fill="#1D2333" stroke="#2C354A" stroke-width="1.2"/>
      <!-- Soft torso highlight -->
      <ellipse cx="-10" cy="-102" rx="16" ry="26" fill="{WHITE}" opacity=".04"/>
      <!-- Cream tee collar & hoodie drawstrings -->
      <path d="M-13 -143 Q0 -130 13 -143" fill="#ECEBE6"/>
      <path d="M-8 -134 L-9 -108 M8 -134 L9 -110" stroke="#9EA7B8" stroke-width="2" stroke-linecap="round" opacity=".65"/>
      <!-- Kangaroo pocket -->
      <path d="M-20 -78 L20 -78 L24 -54 L-24 -54 Z" fill="#171C29" stroke="#283145" stroke-width="1"/>

      <!-- Right arm (relaxed at side -> reaches out to plug cable back in -> cheerful wave!) -->
      <g transform="translate(30 -120)">
        <g class="nitish-fix-arm">
          <path d="M0 0 C18 8 34 14 48 8" fill="none" stroke="#1E2536" stroke-width="16" stroke-linecap="round"/>
          <circle cx="51" cy="7" r="8.5" fill="{SKIN}"/>
        </g>
      </g>

      <!-- Neck -->
      <rect x="-9" y="-156" width="18" height="18" rx="7" fill="{SKIN_DK}"/>

      <!-- Head -->
      <g transform="translate(0 -184)">
        <!-- Ears -->
        <circle cx="-30" cy="4" r="7.5" fill="{SKIN_DK}"/>
        <circle cx="30" cy="4" r="7.5" fill="{SKIN}"/>
        <!-- Face base -->
        <rect x="-30" y="-30" width="60" height="64" rx="28" fill="{SKIN}"/>
        <!-- Warm cheek/forehead highlight -->
        <ellipse cx="6" cy="-6" rx="18" ry="14" fill="{SKIN_LT}" opacity=".35"/>
        <!-- Stylish dark wavy hair -->
        <path d="M-32 -3 C-35 -24 -24 -40 -6 -43 C6 -45 20 -42 28 -30 C35 -20 35 -10 32 -3 C27 -15 16 -21 2 -21 C-14 -21 -25 -15 -32 -3 Z" fill="{HAIR}"/>
        <path d="M-22 -28 C-8 -39 13 -39 24 -25" fill="none" stroke="{HAIR_HI}" stroke-width="4" stroke-linecap="round" opacity=".6"/>
        <!-- Subtle beard/stubble jaw shadow -->
        <path d="M-22 14 C-18 32 18 32 22 14 C16 26 -16 26 -22 14 Z" fill="{HAIR}" opacity=".22"/>
        <!-- Eyes looking toward the chaos on the right -->
        <g>
          <ellipse cx="-9" cy="1" rx="5.2" ry="5.6" fill="{WHITE}"/>
          <ellipse cx="12" cy="1" rx="5.2" ry="5.6" fill="{WHITE}"/>
          <circle cx="-7.2" cy="1.2" r="2.7" fill="{HAIR}"/>
          <circle cx="13.8" cy="1.2" r="2.7" fill="{HAIR}"/>
          <circle cx="-8.2" cy="-0.2" r="1" fill="{WHITE}"/>
          <circle cx="12.8" cy="-0.2" r="1" fill="{WHITE}"/>
        </g>
        <!-- Deadpan eyebrows + dry smirk during chaos -->
        <g class="nitish-deadpan">
          <path d="M-16 -9 L-3 -7" stroke="{HAIR}" stroke-width="2.6" stroke-linecap="round"/>
          <path d="M6 -11 Q13 -15 20 -10" fill="none" stroke="{HAIR}" stroke-width="2.6" stroke-linecap="round"/>
          <path d="M-5 16 Q4 14 11 16" fill="none" stroke="#4A1915" stroke-width="2.4" stroke-linecap="round"/>
        </g>
        <!-- Warm happy grin once fixed -->
        <g class="nitish-happy">
          <path d="M-16 -10 Q-9 -13 -3 -10" fill="none" stroke="{HAIR}" stroke-width="2.4" stroke-linecap="round"/>
          <path d="M6 -10 Q13 -13 19 -10" fill="none" stroke="{HAIR}" stroke-width="2.4" stroke-linecap="round"/>
          <path d="M-7 13 Q3 24 13 13 Z" fill="#4A1915"/>
          <path d="M-5 14 Q3 17 11 14" fill="none" stroke="#F6F1EA" stroke-width="2" stroke-linecap="round"/>
        </g>
      </g>
    </g>
  </g>
</g>"""


def sparky_character():
    """Sparky (Power buddy): amber hard hat that pops off when startled, overalls, holds live plug."""
    return f"""
<g transform="translate(462 {FLOOR_Y})">
  <!-- Ground shadow -->
  <ellipse cx="0" cy="4" rx="44" ry="8.5" fill="#000" opacity=".46"/>

  <g class="sparky-jump">
    <!-- Boots -->
    <rect x="-24" y="-22" width="19" height="22" rx="7" fill="#232A3A"/>
    <rect x="6" y="-22" width="19" height="22" rx="7" fill="#232A3A"/>
    <rect x="-26" y="-5" width="23" height="6" rx="3" fill="{ACCENT}"/>
    <rect x="5" y="-5" width="23" height="6" rx="3" fill="{ACCENT}"/>

    <!-- Plump overalls body -->
    <rect x="-34" y="-92" width="68" height="74" rx="26" fill="#263248" stroke="#364663" stroke-width="1.3"/>
    <!-- Dark tee underneath -->
    <path d="M-24 -92 Q0 -76 24 -92 Z" fill="#141925"/>
    <!-- Overall straps & amber buttons -->
    <rect x="-20" y="-90" width="9" height="32" rx="3" fill="#2F3F5C"/>
    <rect x="11" y="-90" width="9" height="32" rx="3" fill="#2F3F5C"/>
    <circle cx="-15.5" cy="-64" r="3" fill="{ACCENT}"/>
    <circle cx="15.5" cy="-64" r="3" fill="{ACCENT}"/>
    <!-- Pocket with tiny lightning bolt -->
    <rect x="-14" y="-54" width="28" height="20" rx="6" fill="#1E283B"/>
    <path d="M2 -50 L-5 -43 H1 L-2 -36 L6 -44 H0 Z" fill="{ACCENT}"/>

    <!-- Left arm: clutches sparking unplugged cord during chaos, relaxes happily once plugged back in -->
    <g transform="translate(-34 -74)">
      <g class="sparky-mad">
        <!-- Cord curling down from unplugged plug toward floor -->
        <path d="M-36 36 C-26 58 -14 70 8 72" fill="none" stroke="{ACCENT}" stroke-width="4" stroke-linecap="round" opacity=".85"/>
        <path d="M0 0 C-18 6 -30 22 -38 28" fill="none" stroke="#182030" stroke-width="14" stroke-linecap="round"/>
        <circle cx="-40" cy="29" r="8" fill="{SPARKY_SKIN}"/>
        <!-- Giant amber power plug -->
        <g transform="translate(-56 20)">
          <rect x="0" y="0" width="22" height="18" rx="5" fill="{ACCENT}" stroke="#FFD479" stroke-width="1"/>
          <line x1="-8" y1="5" x2="0" y2="5" stroke="#E2E8F0" stroke-width="2.8" stroke-linecap="round"/>
          <line x1="-8" y1="13" x2="0" y2="13" stroke="#E2E8F0" stroke-width="2.8" stroke-linecap="round"/>
          <!-- Angry sparks when unplugged -->
          <path d="M-12 2 L-20 -4 M-14 9 L-23 9 M-12 16 L-19 22" stroke="{ACCENT_MID}" stroke-width="2.2" stroke-linecap="round"/>
        </g>
      </g>
      <g class="sparky-happy">
        <path d="M0 0 C-16 10 -22 24 -14 34" fill="none" stroke="#182030" stroke-width="14" stroke-linecap="round"/>
        <circle cx="-14" cy="36" r="8" fill="{SPARKY_SKIN}"/>
      </g>
    </g>

    <!-- Right arm (points angrily at Chip-Bot during standoff, relaxed when fixed!) -->
    <g transform="translate(34 -74)">
      <g class="sparky-point-arm">
        <path d="M0 0 C22 -8 42 -12 58 -10" fill="none" stroke="#182030" stroke-width="14" stroke-linecap="round"/>
        <circle cx="60" cy="-10" r="8" fill="{SPARKY_SKIN}"/>
        <!-- Pointing finger -->
        <line x1="65" y1="-11" x2="77" y2="-12" stroke="{SPARKY_SKIN}" stroke-width="4.5" stroke-linecap="round"/>
      </g>
      <g class="sparky-chill-arm">
        <path d="M0 0 C16 10 22 24 14 34" fill="none" stroke="#182030" stroke-width="14" stroke-linecap="round"/>
        <circle cx="14" cy="36" r="8" fill="{SPARKY_SKIN}"/>
      </g>
    </g>

    <!-- Head -->
    <g transform="translate(0 -124)">
      <circle cx="-27" cy="2" r="6.5" fill="{SPARKY_SHADE}"/>
      <circle cx="27" cy="2" r="6.5" fill="{SPARKY_SKIN}"/>
      <circle cx="0" cy="0" r="28" fill="{SPARKY_SKIN}"/>
      <ellipse cx="-6" cy="-7" rx="14" ry="10" fill="{WHITE}" opacity=".16"/>
      <!-- Rosy cheeks -->
      <circle cx="-15" cy="8" r="4.5" fill="{BLUSH}" opacity=".28"/>
      <circle cx="15" cy="8" r="4.5" fill="{BLUSH}" opacity=".28"/>

      <!-- Startled/grumpy face during chaos -->
      <g class="sparky-mad">
        <circle cx="-8" cy="-1" r="5.5" fill="{WHITE}"/>
        <circle cx="11" cy="-1" r="5.5" fill="{WHITE}"/>
        <circle cx="-6" cy="-1" r="2.6" fill="#181C24"/>
        <circle cx="13" cy="-1" r="2.6" fill="#181C24"/>
        <circle cx="-7" cy="-2.2" r="1" fill="{WHITE}"/>
        <circle cx="12" cy="-2.2" r="1" fill="{WHITE}"/>
        <!-- Furrowed brows -->
        <path d="M-15 -10 L-3 -6 M18 -10 L6 -6" stroke="#4D2E1B" stroke-width="2.8" stroke-linecap="round"/>
        <!-- Open shouting mouth -->
        <ellipse cx="2" cy="13" rx="6.5" ry="5.5" fill="#4A1915"/>
      </g>

      <!-- Happy relieved face when plugged back in -->
      <g class="sparky-happy">
        <path d="M-13 0 Q-8 -6 -3 0 M6 0 Q11 -6 16 0" fill="none" stroke="#2D1B10" stroke-width="2.8" stroke-linecap="round"/>
        <path d="M-7 10 Q2 20 11 10" fill="none" stroke="#4A1915" stroke-width="2.8" stroke-linecap="round"/>
      </g>

      <!-- Glossy Amber Hard Hat (pops up into the air when startled!) -->
      <g class="hat-pop">
        <path d="M-31 -10 C-31 -34 -16 -44 0 -44 C16 -44 31 -34 31 -10 Z" fill="{ACCENT}"/>
        <!-- Glossy highlight on dome -->
        <path d="M-18 -29 C-12 -36 -2 -38 8 -35" fill="none" stroke="#FFE0B5" stroke-width="4" stroke-linecap="round" opacity=".65"/>
        <!-- Hard hat brim -->
        <rect x="-36" y="-13" width="72" height="8" rx="4" fill="#E67926"/>
        <!-- White lightning emblem -->
        <path d="M2 -34 L-4 -25 H1 L-2 -18 L6 -26 H1 Z" fill="{WHITE}"/>
      </g>
    </g>
  </g>
</g>"""


def chipbot_character():
    """Chip-Bot (Silicon + Robotics buddy): cyan/emerald cute robot with chip-pin ears, gets bonked & points at Nimbus!"""
    return f"""
<g transform="translate(740 {FLOOR_Y})">
  <!-- Ground shadow -->
  <ellipse cx="0" cy="4" rx="46" ry="8.5" fill="#000" opacity=".46"/>

  <g class="bot-react">
    <!-- Cute rubber treads / stubby boots -->
    <rect x="-30" y="-18" width="24" height="18" rx="9" fill="#232D42" stroke="#364563" stroke-width="1.2"/>
    <rect x="6" y="-18" width="24" height="18" rx="9" fill="#232D42" stroke="#364563" stroke-width="1.2"/>
    <circle cx="-18" cy="-9" r="3.5" fill="{ACCENT_2}"/>
    <circle cx="18" cy="-9" r="3.5" fill="{ACCENT_2}"/>

    <!-- Rounded Robot Torso with glowing emerald silicon chip core -->
    <rect x="-34" y="-86" width="68" height="70" rx="22" fill="#182234" stroke="#2D405E" stroke-width="1.5"/>
    <!-- Chest silicon die window -->
    <rect x="-18" y="-68" width="36" height="32" rx="8" fill="#0C111C" stroke="{SILICON}" stroke-width="1.4" stroke-opacity=".8"/>
    <path d="M-18 -58h-5M-18 -46h-5M18 -58h5M18 -46h5M-6 -68v-4M6 -68v-4M-6 -36v4M6 -36v4"
          stroke="{ACCENT_MID}" stroke-width="2" stroke-linecap="round"/>
    <rect x="-9" y="-59" width="18" height="14" rx="3" fill="{SILICON}" opacity=".25"/>
    <circle cx="0" cy="-52" r="4.5" fill="{SILICON}"/>

    <!-- Left arm (flustered hands-up pose clearing gold pins during standoff, waves happily when fixed) -->
    <g transform="translate(-34 -68)">
      <g class="bot-panic-arms">
        <path d="M0 0 C-22 -4 -34 -18 -28 -34" fill="none" stroke="#2B3D5B" stroke-width="12" stroke-linecap="round"/>
        <circle cx="-28" cy="-36" r="7.5" fill="{ACCENT_2}"/>
      </g>
      <g class="bot-happy-arms">
        <path d="M0 0 C-20 -12 -32 -28 -28 -44" fill="none" stroke="#2B3D5B" stroke-width="12" stroke-linecap="round"/>
        <circle cx="-28" cy="-46" r="7.5" fill="{ACCENT_2}"/>
      </g>
    </g>

    <!-- Right arm (pointing directly right at Nimbus during standoff!) -->
    <g transform="translate(34 -68)">
      <g class="bot-panic-arms">
        <path d="M0 0 C22 -12 44 -20 62 -24" fill="none" stroke="#2B3D5B" stroke-width="12" stroke-linecap="round"/>
        <circle cx="64" cy="-24" r="7.5" fill="{ACCENT_2}"/>
        <line x1="69" y1="-26" x2="80" y2="-30" stroke="{ACCENT_2}" stroke-width="4" stroke-linecap="round"/>
      </g>
      <g class="bot-happy-arms">
        <path d="M0 0 C20 -12 32 -28 28 -44" fill="none" stroke="#2B3D5B" stroke-width="12" stroke-linecap="round"/>
        <circle cx="28" cy="-46" r="7.5" fill="{ACCENT_2}"/>
      </g>
    </g>

    <!-- Robot Head -->
    <g transform="translate(0 -122)">
      <!-- Gold IC-pin ears -->
      <rect x="-46" y="-12" width="12" height="5" rx="2.5" fill="{ACCENT_MID}"/>
      <rect x="-46" y="-2" width="12" height="5" rx="2.5" fill="{ACCENT_MID}"/>
      <rect x="-46" y="8" width="12" height="5" rx="2.5" fill="{ACCENT_MID}"/>
      <rect x="34" y="-12" width="12" height="5" rx="2.5" fill="{ACCENT_MID}"/>
      <rect x="34" y="-2" width="12" height="5" rx="2.5" fill="{ACCENT_MID}"/>
      <rect x="34" y="8" width="12" height="5" rx="2.5" fill="{ACCENT_MID}"/>

      <!-- Bouncy antenna -->
      <g class="antenna-wobble">
        <line x1="0" y1="-28" x2="0" y2="-48" stroke="#64748B" stroke-width="3.2" stroke-linecap="round"/>
        <circle cx="0" cy="-52" r="7" fill="{ACCENT_2}"/>
        <circle cx="-2" cy="-54" r="2.2" fill="{WHITE}" opacity=".8"/>
      </g>

      <!-- Cyan helmet shell -->
      <rect x="-38" y="-30" width="76" height="58" rx="22" fill="{ACCENT_2}"/>
      <!-- Soft glossy top rim -->
      <path d="M-22 -24 H22" stroke="#BAE6FD" stroke-width="4" stroke-linecap="round" opacity=".6"/>
      <!-- Dark glossy OLED face visor -->
      <rect x="-30" y="-20" width="60" height="39" rx="14" fill="#0B101B"/>
      <path d="M-22 -14 L-10 -14" stroke="{WHITE}" stroke-width="2.5" stroke-linecap="round" opacity=".2"/>

      <!-- Nervous / panicked eyes + cartoon sweat drop -->
      <g class="bot-nervous">
        <circle cx="-12" cy="-2" r="7" fill="{WHITE}"/>
        <circle cx="12" cy="-2" r="7" fill="{WHITE}"/>
        <!-- Pupils glancing anxiously right at Nimbus -->
        <circle cx="-9.5" cy="-2" r="3" fill="#0B101B"/>
        <circle cx="14.5" cy="-2" r="3" fill="#0B101B"/>
        <circle cx="-10.5" cy="-3.5" r="1.2" fill="{WHITE}"/>
        <circle cx="13.5" cy="-3.5" r="1.2" fill="{WHITE}"/>
        <!-- Squiggly nervous mouth -->
        <path d="M-8 11 Q-4 8 0 11 Q4 14 8 11" fill="none" stroke="{ACCENT}" stroke-width="2.4" stroke-linecap="round"/>
        <!-- Cartoon sweat drop on forehead -->
        <path d="M27 -24 C27 -24 33 -15 33 -11 A6 6 0 1 1 21 -11 C21 -15 27 -24 27 -24 Z" fill="#7DD3FC"/>
      </g>

      <!-- Joyful happy eyes when fixed -->
      <g class="bot-joy">
        <path d="M-19 0 Q-12 -10 -5 0 M5 0 Q12 -10 19 0" fill="none" stroke="{SILICON}" stroke-width="3.4" stroke-linecap="round"/>
        <path d="M-8 9 Q0 16 8 9" fill="none" stroke="{ACCENT_2}" stroke-width="2.8" stroke-linecap="round"/>
      </g>

      <!-- Comic BONK starburst right on top of the antenna when spark hits! -->
      <g transform="translate(0 -54)">
        <g class="bonk-burst">
          <path d="M0 -24 L5 -9 L20 -16 L10 -3 L25 4 L9 7 L14 21 L1 10 L-12 21 L-8 7 L-24 4 L-10 -3 L-19 -16 L-5 -9 Z"
                fill="{ACCENT_MID}" stroke="{RED}" stroke-width="1.8" stroke-linejoin="round"/>
        </g>
      </g>
    </g>
  </g>
</g>"""


def nimbus_character():
    """Nimbus (Cloud buddy): fluffy violet cloud floating above sneakers, drops spark then whistles innocently."""
    return f"""
<g transform="translate(1004 {FLOOR_Y})">
  <!-- Soft hovering shadow on floor -->
  <ellipse class="cloud-shadow" cx="0" cy="4" rx="44" ry="7.5" fill="#000" opacity=".36"/>

  <g class="cloud-float">
    <!-- Little dangling sneakers kicking gently in midair -->
    <g transform="translate(0 -54)">
      <path d="M-14 -10 L-18 14" stroke="#6D5CAE" stroke-width="6.5" stroke-linecap="round"/>
      <path d="M14 -10 L18 14" stroke="#6D5CAE" stroke-width="6.5" stroke-linecap="round"/>
      <ellipse cx="-21" cy="18" rx="12" ry="7" fill="{ACCENT}"/>
      <ellipse cx="21" cy="18" rx="12" ry="7" fill="{ACCENT}"/>
      <line x1="-30" y1="22" x2="-12" y2="22" stroke="{WHITE}" stroke-width="2.5" stroke-linecap="round"/>
      <line x1="12" y1="22" x2="30" y2="22" stroke="{WHITE}" stroke-width="2.5" stroke-linecap="round"/>
    </g>

    <!-- Fluffy multi-lobe illustrated cloud body -->
    <g transform="translate(0 -116)">
      <!-- Main cloud silhouette -->
      <path d="M-48 26 H48 C64 26 74 14 72 -2 C70 -16 58 -24 44 -22 C40 -42 22 -54 2 -52 C-16 -50 -28 -38 -32 -24 C-48 -28 -64 -16 -66 0 C-68 16 -58 26 -48 26 Z"
            fill="url(#cloudGrad)" stroke="#C8B9FF" stroke-width="1.3" stroke-linejoin="round"/>
      <!-- Soft top highlights -->
      <ellipse cx="-14" cy="-26" rx="20" ry="12" fill="{WHITE}" opacity=".2"/>
      <ellipse cx="32" cy="-8" rx="14" ry="9" fill="{WHITE}" opacity=".14"/>

      <!-- Innocent whistling face (looking far right away from the crime scene!) -->
      <g class="cloud-whistle">
        <ellipse cx="-12" cy="-6" rx="6.2" ry="6.6" fill="{WHITE}"/>
        <ellipse cx="14" cy="-6" rx="6.2" ry="6.6" fill="{WHITE}"/>
        <!-- Pupils glancing way over to the right -->
        <circle cx="-8.5" cy="-7" r="3" fill="#1A1530"/>
        <circle cx="17.5" cy="-7" r="3" fill="#1A1530"/>
        <circle cx="-9.5" cy="-8.5" r="1.1" fill="{WHITE}"/>
        <circle cx="16.5" cy="-8.5" r="1.1" fill="{WHITE}"/>
        <!-- Relaxed innocent brows -->
        <path d="M-19 -16 Q-12 -20 -6 -16 M8 -16 Q14 -20 20 -16" fill="none" stroke="#45337A" stroke-width="2.4" stroke-linecap="round"/>
        <!-- Tiny whistling 'o' mouth -->
        <circle cx="6" cy="9" r="3.6" fill="#3B296E"/>
        <!-- Floating musical notes drifting right out of the whistle! -->
        <g class="music-notes">
          <text x="34" y="-12" font-family="{SANS}" font-size="22" font-weight="700" fill="{ACCENT_MID}">♪</text>
          <text x="58" y="-32" font-family="{SANS}" font-size="18" font-weight="700" fill="{ACCENT_2}">♫</text>
        </g>
      </g>

      <!-- Sheepish / happy face once fixed -->
      <g class="cloud-sheepish">
        <path d="M-18 -6 Q-12 -13 -6 -6 M8 -6 Q14 -13 20 -6" fill="none" stroke="#2D1E59" stroke-width="2.8" stroke-linecap="round"/>
        <ellipse cx="-22" cy="4" rx="7" ry="4" fill="{BLUSH}" opacity=".55"/>
        <ellipse cx="24" cy="4" rx="7" ry="4" fill="{BLUSH}" opacity=".55"/>
        <path d="M-6 6 Q2 14 10 6" fill="none" stroke="#3B296E" stroke-width="2.6" stroke-linecap="round"/>
      </g>
    </g>
  </g>
</g>"""


def build():
    css = [
        # Subtle coffee steam drift
        "@keyframes steam{0%{transform:translateY(0);opacity:.45}100%{transform:translateY(-10px);opacity:0}}",
        ".steam{animation:steam 2.4s ease-out infinite}",
        # Floating music notes gentle bob
        "@keyframes notes{0%,100%{transform:translate(0,0) rotate(-4deg)}50%{transform:translate(4px,-8px) rotate(6deg)}}",
        ".music-notes{animation:notes 1.8s ease-in-out infinite}",
        # Gentle breathing bob on Nitish
        "@keyframes nbob{0%,100%{transform:translateY(0)}50%{transform:translateY(-2.5px)}}",
        ".nitish-bob{animation:nbob 3.2s ease-in-out infinite}",
    ]

    # ---- Master Choreography Keyframes (13.0s cycle, phase-shifted -5.4s) ------------------
    # 0.0 - 1.6s: Nimbus drops glowing hot spark -> parabolic arc onto Chip-Bot's antenna
    # 1.6 - 2.3s: BONK! Chip-Bot jumps & accidentally yanks cord from Sparky
    # 2.3 - 7.8s: PEAK 4-CHARACTER STANDOFF (t=0 lands right here at 5.4s!)
    #             Sparky yells "Hey!!", Chip-Bot points "He started it!",
    #             Nimbus whistles "Wasn't me.", Nitish sighs "Every time..."
    # 7.8 - 9.8s: Nitish walks over, reaches out & plugs the cord back in!
    # 9.8 - 13.0s: Warm power wave restores everyone; Nimbus blushes "My bad.", everyone cheers!

    # 1. Dropped spark arc from Nimbus (952, 240) -> Chip-Bot antenna (740, 180)
    css.append(kf("spark_drop", [
        (0.0,   "transform:translate(952px,240px) scale(0.9);opacity:0"),
        (0.25,  "transform:translate(952px,240px) scale(1);opacity:1"),
        (0.75,  "transform:translate(918px,186px) scale(1.05);opacity:1"),
        (1.25,  "transform:translate(825px,136px) scale(1.1);opacity:1"),
        (1.62,  "transform:translate(740px,180px) scale(1.25);opacity:1"),
        (1.78,  "transform:translate(740px,180px) scale(0.3);opacity:0"),
        (CYCLE, "transform:translate(952px,240px) scale(0.9);opacity:0"),
    ]))
    css.append(f".spark-drop{{{anim('spark_drop', 'ease-in-out')}}}")

    # 2. Comic BONK starburst on Chip-Bot's antenna
    css.append(kf("bonk_burst", [
        (0.0,   "opacity:0;transform:scale(.3)"),
        (1.55,  "opacity:0;transform:scale(.3)"),
        (1.68,  "opacity:1;transform:scale(1.15)"),
        (2.15,  "opacity:1;transform:scale(.95)"),
        (2.38,  "opacity:0;transform:scale(.4)"),
        (CYCLE, "opacity:0;transform:scale(.3)"),
    ]))
    css.append(f".bonk-burst{{{anim('bonk_burst', 'ease-out')}}}")

    # 3. Nitish walk over to plug in cord (7.8s..10.4s) & arm reach
    css.append(kf("nitish_walk", [
        (0.0,   "transform:translateX(0px)"),
        (7.70,  "transform:translateX(0px)"),
        (8.65,  "transform:translateX(118px)"),
        (9.35,  "transform:translateX(118px)"),
        (10.45, "transform:translateX(0px)"),
        (CYCLE, "transform:translateX(0px)"),
    ]))
    css.append(f".nitish-walk{{{anim('nitish_walk', 'ease-in-out')}}}")

    css.append(kf("nitish_fix_arm", [
        (0.0,   "transform:rotate(58deg)"),
        (7.80,  "transform:rotate(58deg)"),
        (8.65,  "transform:rotate(14deg)"),
        (9.10,  "transform:rotate(24deg)"),
        (9.60,  "transform:rotate(-28deg)"),  # cheerful little wave!
        (11.60, "transform:rotate(-28deg)"),
        (12.25, "transform:rotate(58deg)"),
        (CYCLE, "transform:rotate(58deg)"),
    ]))
    css.append(f".nitish-fix-arm{{{anim('nitish_fix_arm', 'ease-in-out')}}}")

    # Nitish expression swap: deadpan (2.2s..9.1s) vs happy (9.1s..13s & 0..2.2s)
    css.append(kf("nitish_deadpan", [
        (0.0, "opacity:0"), (2.1, "opacity:0"), (2.3, "opacity:1"),
        (8.95, "opacity:1"), (9.15, "opacity:0"), (CYCLE, "opacity:0"),
    ]))
    css.append(f".nitish-deadpan{{{anim('nitish_deadpan', 'linear')}}}")

    css.append(kf("nitish_happy", [
        (0.0, "opacity:1"), (2.1, "opacity:1"), (2.3, "opacity:0"),
        (8.95, "opacity:0"), (9.15, "opacity:1"), (CYCLE, "opacity:1"),
    ]))
    css.append(f".nitish-happy{{{anim('nitish_happy', 'linear')}}}")

    # 4. Sparky jump, hard hat pop, plug wiggle, and angry vs happy states
    css.append(kf("sparky_jump", [
        (0.0,   "transform:translateY(0px)"),
        (2.00,  "transform:translateY(0px)"),
        (2.25,  "transform:translateY(-20px)"),
        (2.55,  "transform:translateY(0px)"),
        (9.10,  "transform:translateY(0px)"),
        (9.35,  "transform:translateY(-10px)"),
        (9.65,  "transform:translateY(0px)"),
        (CYCLE, "transform:translateY(0px)"),
    ]))
    css.append(f".sparky-jump{{{anim('sparky_jump', 'ease-out')}}}")

    css.append(kf("hat_pop", [
        (0.0,   "transform:translateY(0px) rotate(0deg)"),
        (2.05,  "transform:translateY(0px) rotate(0deg)"),
        (2.35,  "transform:translateY(-20px) rotate(-10deg)"),
        (2.75,  "transform:translateY(-10px) rotate(-7deg)"),
        (8.90,  "transform:translateY(-10px) rotate(-7deg)"),
        (9.20,  "transform:translateY(0px) rotate(0deg)"),
        (CYCLE, "transform:translateY(0px) rotate(0deg)"),
    ]))
    css.append(f".hat-pop{{{anim('hat_pop', 'ease-out')}}}")

    css.append(kf("sparky_mad", [
        (0.0, "opacity:0"), (2.0, "opacity:0"), (2.15, "opacity:1"),
        (8.95, "opacity:1"), (9.15, "opacity:0"), (CYCLE, "opacity:0"),
    ]))
    css.append(f".sparky-mad,.sparky-point-arm{{{anim('sparky_mad', 'linear')}}}")

    css.append(kf("sparky_happy", [
        (0.0, "opacity:1"), (2.0, "opacity:1"), (2.15, "opacity:0"),
        (8.95, "opacity:0"), (9.15, "opacity:1"), (CYCLE, "opacity:1"),
    ]))
    css.append(f".sparky-happy,.sparky-chill-arm{{{anim('sparky_happy', 'linear')}}}")

    # 5. Chip-Bot bonk squash, nervous vs joy states, antenna wobble
    css.append(kf("bot_react", [
        (0.0,   "transform:translateY(0px) rotate(0deg)"),
        (1.60,  "transform:translateY(0px) rotate(0deg)"),
        (1.78,  "transform:translateY(7px) rotate(-6deg)"),
        (2.10,  "transform:translateY(-8px) rotate(4deg)"),
        (2.40,  "transform:translateY(0px) rotate(-2deg)"),
        (9.10,  "transform:translateY(0px) rotate(-2deg)"),
        (9.45,  "transform:translateY(-14px) rotate(0deg)"),
        (9.80,  "transform:translateY(0px) rotate(0deg)"),
        (10.15, "transform:translateY(-8px) rotate(0deg)"),
        (10.50, "transform:translateY(0px) rotate(0deg)"),
        (CYCLE, "transform:translateY(0px) rotate(0deg)"),
    ]))
    css.append(f".bot-react{{{anim('bot_react', 'ease-in-out')}}}")

    css.append(kf("antenna_wobble", [
        (0.0,   "transform:rotate(0deg)"),
        (1.62,  "transform:rotate(0deg)"),
        (1.76,  "transform:rotate(-24deg)"),
        (1.94,  "transform:rotate(20deg)"),
        (2.14,  "transform:rotate(-14deg)"),
        (2.38,  "transform:rotate(6deg)"),
        (2.65,  "transform:rotate(0deg)"),
        (CYCLE, "transform:rotate(0deg)"),
    ]))
    css.append(f".antenna-wobble{{{anim('antenna_wobble', 'ease-in-out')}}}")

    css.append(kf("bot_nervous", [
        (0.0, "opacity:0"), (1.62, "opacity:0"), (1.75, "opacity:1"),
        (9.20, "opacity:1"), (9.40, "opacity:0"), (CYCLE, "opacity:0"),
    ]))
    css.append(f".bot-nervous,.bot-panic-arms{{{anim('bot_nervous', 'linear')}}}")

    css.append(kf("bot_joy", [
        (0.0, "opacity:1"), (1.62, "opacity:1"), (1.75, "opacity:0"),
        (9.20, "opacity:0"), (9.40, "opacity:1"), (CYCLE, "opacity:1"),
    ]))
    css.append(f".bot-joy,.bot-happy-arms{{{anim('bot_joy', 'linear')}}}")

    # 6. Nimbus float, whistle innocently during standoff, sheepish blush once fixed
    css.append(kf("cloud_float", [
        (0.0,   "transform:translateY(0px)"),
        (2.20,  "transform:translateY(-4px)"),
        (4.50,  "transform:translateY(-14px)"),
        (7.50,  "transform:translateY(-10px)"),
        (9.50,  "transform:translateY(2px)"),
        (11.40, "transform:translateY(-7px)"),
        (CYCLE, "transform:translateY(0px)"),
    ]))
    css.append(f".cloud-float{{{anim('cloud_float', 'ease-in-out')}}}")

    css.append(kf("cloud_whistle", [
        (0.0, "opacity:0"), (2.15, "opacity:0"), (2.35, "opacity:1"),
        (9.35, "opacity:1"), (9.55, "opacity:0"), (CYCLE, "opacity:0"),
    ]))
    css.append(f".cloud-whistle{{{anim('cloud_whistle', 'linear')}}}")

    css.append(kf("cloud_sheepish", [
        (0.0, "opacity:1"), (2.15, "opacity:1"), (2.35, "opacity:0"),
        (9.35, "opacity:0"), (9.55, "opacity:1"), (CYCLE, "opacity:1"),
    ]))
    css.append(f".cloud-sheepish{{{anim('cloud_sheepish', 'linear')}}}")

    # 7. Speech Bubbles (natural comic pacing, all 4 visible together during the standoff!)
    def bubble_kf(name, t_in, t_out):
        css.append(kf(name, [
            (0.0,         "opacity:0;transform:translateY(8px) scale(.9)"),
            (t_in - 0.10, "opacity:0;transform:translateY(8px) scale(.9)"),
            (t_in + 0.16, "opacity:1;transform:translateY(0px) scale(1)"),
            (t_out - 0.15,"opacity:1;transform:translateY(0px) scale(1)"),
            (t_out + 0.08,"opacity:0;transform:translateY(-5px) scale(.92)"),
            (CYCLE,       "opacity:0;transform:translateY(8px) scale(.9)"),
        ]))
        css.append(f".{name}{{{anim(name, 'ease-out')}}}")

    bubble_kf("bub-sparky", 2.25, 8.85)   # "Hey!!"
    bubble_kf("bub-bot",    2.70, 9.05)   # "He started it!"
    bubble_kf("bub-cloud",  3.15, 9.25)   # "Wasn't me."
    bubble_kf("bub-nitish", 3.65, 7.65)   # "Every time…"
    bubble_kf("bub-mybad",  9.55, 12.10)  # "My bad." (from Nimbus after fix!)
    bubble_kf("bub-allgood",9.75, 12.30)  # "All good!" (from Nitish!)

    # 8. Restoring power pulse along the floor cable when Nitish plugs it in (9.0s..11.2s)
    css.append(kf("power_pulse", [
        (0.0,   "opacity:0;transform:translate(356px,348px)"),
        (8.95,  "opacity:0;transform:translate(356px,348px)"),
        (9.10,  "opacity:1;transform:translate(356px,348px)"),
        (9.75,  "opacity:1;transform:translate(740px,348px)"),
        (10.35, "opacity:1;transform:translate(940px,289px)"),
        (10.70, "opacity:0;transform:translate(985px,259px)"),
        (CYCLE, "opacity:0;transform:translate(356px,348px)"),
    ]))
    css.append(f".power-pulse{{{anim('power_pulse', 'ease-in-out')}}}")

    css.append(kf("cable_live", [
        (0.0, "opacity:.85"), (2.05, "opacity:.85"), (2.20, "opacity:.18"),
        (8.95, "opacity:.18"), (9.15, "opacity:.95"), (CYCLE, "opacity:.85"),
    ]))
    css.append(f".cable-live{{{anim('cable_live', 'linear')}}}")

    css.append(
        "@media (prefers-reduced-motion: reduce){"
        "*{animation-play-state:paused!important}}"
    )

    # ---- Stage Floor & Interactive Cable Props ---------------------------------------------
    stage_props = f"""
<!-- Studio floor horizon -->
<rect x="0" y="320" width="{W}" height="{H - 320}" fill="url(#floorGrad)"/>
<line x1="48" y1="320" x2="{W - 48}" y2="320" stroke="{WHITE}" stroke-opacity=".065"/>

<!-- Coiled floor cable connecting Power -> Chip-Bot -> wireless link to Nimbus -->
<path d="M356 346 C460 366 590 338 740 348" fill="none" stroke="#1E2638" stroke-width="5" stroke-linecap="round"/>
<path class="cable-live" d="M356 346 C460 366 590 338 740 348" fill="none" stroke="url(#cableGrad)" stroke-width="2.6" stroke-linecap="round"/>
<path class="cable-live" d="M774 338 C856 330 916 304 962 268" fill="none" stroke="{ACCENT_2}" stroke-width="2.2" stroke-dasharray="5 7" stroke-linecap="round"/>

<!-- Floor power junction box (where Nitish plugs Sparky's cord back in!) -->
<g transform="translate(342 330)">
  <rect x="-14" y="0" width="28" height="24" rx="6" fill="#171E2E" stroke="#2D384F" stroke-width="1.3"/>
  <circle cx="0" cy="12" r="4" fill="{GREEN}" class="cable-live"/>
  <!-- Snapped-in amber plug when power is live -->
  <g class="sparky-happy">
    <rect x="13" y="5" width="16" height="14" rx="4" fill="{ACCENT}" stroke="#FFD479" stroke-width="1"/>
  </g>
</g>

<!-- Restoring bright pulse traveling through the system -->
<g class="power-pulse">
  <circle cx="0" cy="0" r="14" fill="{ACCENT}" opacity=".35"/>
  <circle cx="0" cy="0" r="5" fill="{WHITE}"/>
</g>"""

    # ---- Dropped hot spark prop (Nimbus -> Chip-Bot) ---------------------------------------
    dropped_spark = f"""
<g class="spark-drop">
  <circle cx="0" cy="0" r="16" fill="{RED}" opacity=".28"/>
  <path d="M0 -11 L3 -3 L11 -4 L5 2 L8 10 L0 5 L-8 10 L-5 2 L-11 -4 L-3 -3 Z" fill="{ACCENT_MID}" stroke="{RED}" stroke-width="1.4" stroke-linejoin="round"/>
</g>"""

    # ---- All Comic Speech Bubbles (friendly sentence case, zero all-caps!) -----------------
    bubbles = "".join([
        bubble(184, 78,  126, "Every time…",    tail_dx=-4, cls="bub-nitish",  accent="#3A445C"),
        bubble(184, 78,  110, "All good!",      tail_dx=-4, cls="bub-allgood", accent=GREEN),
        bubble(464, 118, 86,  "Hey!!",          tail_dx=0,  cls="bub-sparky",  accent=ACCENT),
        bubble(742, 106, 146, "He started it!", tail_dx=-2, cls="bub-bot",     accent=ACCENT_2),
        bubble(998, 96,  122, "Wasn't me.",     tail_dx=4,  cls="bub-cloud",   accent=VIOLET),
        bubble(998, 96,  106, "My bad.",        tail_dx=4,  cls="bub-mybad",   accent=BLUSH),
    ])

    # ---- Quiet, understated corner signature (no SaaS chrome, no all-caps!) ----------------
    quiet_footer = f"""
<text x="36" y="{H - 22}" font-family="{SANS}" font-size="13.5" font-weight="500" fill="#6D778C">nitish sundarraj</text>
<text x="{W - 56}" y="{H - 22}" text-anchor="end" font-family="{SANS}" font-size="13.5" font-weight="500" fill="#6D778C">portfolio</text>
<path d="M{W - 48} {H - 26.5} h11 m-4 -4 l4 4 l-4 4" fill="none" stroke="{ACCENT}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>"""

    body = f"""<defs>
<clipPath id="frame"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="21"/></clipPath>
<linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#0D1018"/>
  <stop offset="1" stop-color="#07090E"/>
</linearGradient>
<linearGradient id="floorGrad" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#111622"/>
  <stop offset="1" stop-color="#080A10"/>
</linearGradient>
<linearGradient id="cloudGrad" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#C6B8FF"/>
  <stop offset=".6" stop-color="#9B86F5"/>
  <stop offset="1" stop-color="#7660D4"/>
</linearGradient>
<linearGradient id="cableGrad" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{ACCENT}"/>
  <stop offset=".5" stop-color="{SILICON}"/>
  <stop offset="1" stop-color="{ACCENT_2}"/>
</linearGradient>
<radialGradient id="spotWarm" cx="34%" cy="56%" r="40%">
  <stop offset="0" stop-color="{ACCENT}" stop-opacity=".10"/>
  <stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/>
</radialGradient>
<radialGradient id="spotCool" cx="76%" cy="48%" r="42%">
  <stop offset="0" stop-color="{ACCENT_2}" stop-opacity=".09"/>
  <stop offset="1" stop-color="{ACCENT_2}" stop-opacity="0"/>
</radialGradient>
<radialGradient id="spotViolet" cx="88%" cy="38%" r="32%">
  <stop offset="0" stop-color="{VIOLET}" stop-opacity=".10"/>
  <stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/>
</radialGradient>
</defs>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="22" fill="url(#bgGrad)" stroke="#1D2332"/>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="url(#spotWarm)"/>
  <rect width="{W}" height="{H}" fill="url(#spotCool)"/>
  <rect width="{W}" height="{H}" fill="url(#spotViolet)"/>
  {stage_props}
  {nitish_character()}
  {sparky_character()}
  {chipbot_character()}
  {nimbus_character()}
  {dropped_spark}
  {bubbles}
  {quiet_footer}
</g>"""

    return doc(
        W, H,
        "Nitish Sundarraj — workshop characters",
        "\n".join(css),
        body,
        "Four illustrated characters interacting on a dark workshop stage: a floating cloud buddy drops a hot spark "
        "onto a little robot, who yanks the power buddy's cord, sparking a comic finger-pointing standoff while "
        "Nitish sighs over his coffee and walks over to plug everything back in."
    )
