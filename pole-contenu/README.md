# Pôle Contenu ESGDR — agents IA

Six agents Claude Code spécialisés, réunis dans un même pôle, pour produire du contenu **entraînement football & méthodologie**.

| Agent | Fichier | Rôle |
|---|---|---|
| Format des posts | `.claude/agents/format-posts.md` | Choisit le format (carrousel, citation, infographie…), écrit hook, slides, légende, hashtags |
| Design des posts | `.claude/agents/design-posts.md` | Direction artistique navy/or, mise en page slide par slide, schémas tactiques, Canva |
| Format des vidéos | `.claude/agents/format-videos.md` | Choisit le format vidéo, écrit hook, script, découpage plan par plan |
| Design des vidéos | `.claude/agents/design-videos.md` | Sous-titres, incrustations, rythme de montage, cover/miniature |
| Son des vidéos | `.claude/agents/son-videos.md` | Musique sous licence, sound design, voix, mixage |
| Publication | `.claude/agents/publication.md` | Bonne plateforme, bon jour, bonne heure selon la niche et la saison |

Référence commune : [`charte.md`](charte.md) (identité, couleurs, ton, règles).

## Utilisation

**Tout le pôle d'un coup** (dans Claude Code, à la racine du dépôt) :

```
/pole-contenu Rondo 4c2 avec transition pour U15
```

Le skill `pole-contenu` enchaîne les six agents et dépose les fiches dans `pole-contenu/livrables/<date>-<sujet>/`.

**Un agent seul** :

```
Utilise l'agent publication pour planifier mes 3 Reels de la semaine prochaine.
Demande à son-videos une ambiance sonore pour ma vidéo d'échauffement.
```

## Personnaliser

- Modifier les couleurs, le ton ou les plateformes : `charte.md` (tous les agents suivent).
- Ajuster les créneaux horaires avec vos vraies stats : tableau dans `.claude/agents/publication.md`.
