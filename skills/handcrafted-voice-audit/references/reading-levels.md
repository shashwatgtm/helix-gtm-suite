# Setting the reading level per audience

The reading level is set for the readers, not for the writer. The same facts can be written at two levels for two audiences.

| Audience | Band to aim for | What that means in practice |
|---|---|---|
| Field and frontline teams, broad social media readers, mixed language readers | secondary school | short sentences, common words, one idea per sentence |
| Readers not named (the default when no audience is given); once an audience is named, use the named audience table below instead | secondary school to graduate | plain words, some sentences longer, sector terms the readers use every day |
| Boards, CXOs reading a long form brief, specialist peers | graduate | longer reasoning is fine; still no jargon the reader would not use |

## Named audiences: one specific band each

When the user names an audience, pick the row that matches the readers and the channel, set that one band, and name the row in the answer. The band is a ceiling: text above it is lowered with the steps below; text already below it is not made harder. The script's band names and grade ranges (scripts/voice_scan.py) are used so the re-scan can be compared with the band directly. These rows are a working method for this skill, not a measured standard.

| Named audience and channel | Specific band | Script grade to stay under |
|---|---|---|
| Frontline and field teams, new reps, broad social media readers, mixed language readers | secondary school | 10 |
| Functional leaders and managers reading a social post, a newsletter or a blog (for example sales leaders, HR leaders, heads of delivery, contact center leaders, marketing leaders) | upper secondary | 13 |
| Specialist buyers reading long form in their own field (for example CIOs, CISOs, risk and compliance heads at banks and insurers reading a company blog or a brief) | upper secondary, with the sector terms these readers use every day | 13 |
| Boards, CXOs reading a long form brief, specialist peers reading technical long form | graduate | 17 |

An audience that fits no row: choose the nearest row by role and channel, say which row was used and why, and offer one question to confirm it. Two audiences for one text (for example field teams and their managers): use the lower band.

How to use the script's grade:
- scripts/voice_scan.py reports an approximate reading grade (the Flesch Kincaid formula with a simple syllable count) and a band name. It is an estimate. It is a signal to look again, not a verdict.
- Short texts (under about 60 words) give unstable grades; say so instead of reporting them as precise.
- Names, product terms and quoted text raise the grade without making the text harder for its readers. Run with --skip-quotes when quotes are long.

How to lower the level without losing the writer's voice:
- Split long sentences at "and", "but" or "because", keeping the writer's own words.
- Replace a rare word with the word the reader would use, only where it was flagged.
- Do not cut emotion or the writer's own phrasing to lower the grade.

When no audience is given: use the default band, say so in one line, and offer one question about the audience at the end. If the user asked for no questions, replace the question with one line saying the band can be reset once they name the readers.
