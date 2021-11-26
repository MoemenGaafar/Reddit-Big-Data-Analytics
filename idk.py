from riotwatcher import LolWatcher
player_puuid = 'rPJiRKIgBqDvMeaF-oWRlIRG8TC3hkNKWNRN6fYByXmYr2XSUL2NWgP95ZcAhMv5WzOOSRgTeQCByg'
RiotKey = 'RGAPI-f69c2e1a-2d77-448e-b660-39a330071734'
watcher = LolWatcher(RiotKey)
matches = watcher.match.matchlist_by_puuid("europe", player_puuid)
print(matches)