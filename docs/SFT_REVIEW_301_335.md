# Hand review: SFT pairs sft_301–sft_335 (added 2026-11-13)

For each pair: is the answer correct, supported by the source (or by the scope policy), short and in the assistant's voice? Is it different from every test question? Mark ✅ keep / ✏️ fix / ❌ remove, then update `human_review_status` in `data/sft_pairs.jsonl`.

## sft_301 · online_profile_length · train
**Q:** I'm a first-year student. Does my LinkedIn profile need to be long?

**A:** No. A student profile can be brief, and two or three items is fine. Add internships, summer jobs or awards as you earn them, and keep every detail honest and accurate.

Source: `data/cpt/documents/openstax_cs_resumes_and_online_profiles.txt` — “a college student’s can be brief”

Review: ☐ keep ☐ fix ☐ remove

## sft_302 · online_profile_vs_cv · train
**Q:** Can my LinkedIn profile replace my CV when I apply for a job?

**A:** No. An online profile helps you make professional connections, but it does not replace a CV. Keep both up to date and make sure the information matches.

Source: `data/cpt/documents/openstax_cs_resumes_and_online_profiles.txt` — “LinkedIn is not a replacement for a real resume.”

Review: ☐ keep ☐ fix ☐ remove

## sft_303 · online_profile_connections · train
**Q:** Should I send LinkedIn connection requests to many alumni I have never met?

**A:** It is better not to. Connect with people you have met or worked with, and add a short personal note to each invitation instead of sending many requests to strangers.

Source: `data/cpt/documents/openstax_cs_resumes_and_online_profiles.txt` — “adding a personal note on the invite message”

Review: ☐ keep ☐ fix ☐ remove

## sft_304 · social_media_review · train
**Q:** I'm about to apply for internships. Should I check my public social media first?

**A:** Yes. Employers may look at what you post and share. Review your public accounts, remove anything you would not want an employer to see, and consider making personal profiles private.

Source: `data/cpt/documents/openstax_ib_resume_keywords_and_online_presence.txt` — “set all of your personal social media profiles to private”

Review: ☐ keep ☐ fix ☐ remove

## sft_305 · online_profile_photo · train
**Q:** Is it fine to use a funny party photo as my LinkedIn picture?

**A:** It is better to choose a professional photo. Keep your professional profile professional rather than personal, because employers may view it alongside your CV.

Source: `data/cpt/documents/openstax_cs_resumes_and_online_profiles.txt` — “keep it professional, not personal”

Review: ☐ keep ☐ fix ☐ remove

## sft_306 · upload_readability · train
**Q:** I designed a CV full of icons and graphics. Is there a risk when I upload it to a company website?

**A:** Yes. Many companies scan uploaded CVs with software that looks for keywords, experience and skills, and this software may not read drawings and designs well. A plain, text-based version is safer for online applications.

Source: `data/cpt/documents/openstax_wss_resume_presentation_and_letterhead.txt` — “These computer programs do not read drawings and designs well”

Review: ☐ keep ☐ fix ☐ remove

## sft_307 · letterhead_consistency · train
**Q:** Should my printed CV and cover letter use the same header design?

**A:** Yes. Using the same personal letterhead on all your application documents looks professional and makes them clearly belong together.

Source: `data/cpt/documents/openstax_wss_resume_presentation_and_letterhead.txt` — “Using a consistent letterhead across all your communications will add a look of professionalism”

Review: ☐ keep ☐ fix ☐ remove

## sft_308 · military_service · train
**Q:** I did military service before starting university. Should it go on my CV?

**A:** Usually yes. Military or similar service is nearly always worth including, and you can describe the responsibilities and transferable skills it gave you.

Source: `data/cpt/documents/openstax_cs_resumes_and_online_profiles.txt` — “Military service or similar experience should nearly always be included.”

Review: ☐ keep ☐ fix ☐ remove

## sft_309 · identify_strengths · train
**Q:** Before I write my CV, how can I work out which strengths to highlight?

**A:** Notice tasks you do well and enjoy, think about what people usually come to you for, and ask friends, teachers or supervisors what they see as your strengths. Then choose real examples that show those strengths.

Source: `data/cpt/documents/openstax_cs_knowing_your_strengths.txt` — “Ask people who know you to tell you what they think your strengths are.”

Review: ☐ keep ☐ fix ☐ remove

## sft_310 · ksa_meaning · train
**Q:** What does KSAs mean in career planning?

**A:** KSAs are your Knowledge, Skills and Abilities: what you know, what you can do and how well you can do it. A CV should give evidence of them, not just claim them.

Source: `data/cpt/documents/openstax_cs_knowing_your_strengths.txt` — “Think of these as your Knowledge, Skills, and Abilities (KSAs).”

Review: ☐ keep ☐ fix ☐ remove

## sft_311 · experience_journal · train
**Q:** How can I make it easier to write CV bullets about my internship after it ends?

**A:** Keep a short journal during the internship. Note the tasks you did, what you learned and where you did well, and save documents you produced. These notes give you accurate details for your bullets later.

Source: `data/cpt/documents/openstax_cs_building_transferable_skills.txt` — “Jot down some anecdotes, events, and tasks you performed.”

Review: ☐ keep ☐ fix ☐ remove

## sft_312 · avoid_generic_cv · train
**Q:** Can I send exactly the same CV to every employer?

**A:** It is better to adjust it for each application. Highlight the most relevant parts, change the order of details, or emphasise key facts so the CV does not read like a one-size-fits-all document.

Source: `data/cpt/documents/openstax_wg_persuasive_resume_and_career_goal.txt` — “The résumé should not be a one-size-fits-all product”

Review: ☐ keep ☐ fix ☐ remove

## sft_313 · keyword_type · train
**Q:** Are applicant tracking system keywords mostly action verbs?

**A:** Not mainly. Keywords are usually nouns or noun phrases used in the field, such as job titles, tools or methods. Action verbs still help the people who read your CV.

Source: `data/cpt/documents/openstax_ib_resume_keywords_and_online_presence.txt` — “Keywords tend to be more of the noun or noun phrase type”

Review: ☐ keep ☐ fix ☐ remove

## sft_314 · technical_skill_list · train
**Q:** For a technical internship, how can I list my software skills?

**A:** You can list them as nouns or short phrases separated by commas, for example "Python, Excel, SQL". Where it helps, add an accomplishment that shows how you used them.

Source: `data/cpt/documents/openstax_ib_resume_keywords_and_online_presence.txt` — “you can list your skills, separating each noun or phrase by a comma”

Review: ☐ keep ☐ fix ☐ remove

## sft_315 · outside_review · train
**Q:** Who should look at my first CV before I send it?

**A:** Ask a career counselor or someone who knows the field to check the format and look for mistakes. Websites are useful, but another reader often notices problems you miss.

Source: `data/cpt/documents/openstax_cs_resumes_and_online_profiles.txt` — “be sure to run your résume by others”

Review: ☐ keep ☐ fix ☐ remove

## sft_316 · creative_field_portfolio · train
**Q:** I'm studying graphic design. Is a standard one-page document enough to show my work?

**A:** In creative fields, a multimedia résumé or a professional website that shows your work can help. Keep a standard CV as well for applications that ask for one.

Source: `data/cpt/documents/openstax_ib_resume_keywords_and_online_presence.txt` — “a multimedia résumé might be a good choice”

Review: ☐ keep ☐ fix ☐ remove

## sft_317 · career_goal_statement · validation
**Q:** How should a one-line career goal at the top of my CV sound?

**A:** Decisive and focused on what you can contribute. For example: "To use my programming skills to create useful content for a growing company."

Source: `data/cpt/documents/openstax_wg_persuasive_resume_and_career_goal.txt` — “try to stand out by sounding decisive”

Review: ☐ keep ☐ fix ☐ remove

## sft_318 · career_goal_statement · validation
**Q:** Can I change my career goal statement for different applications?

**A:** Yes. A reader may skim your CV for only a few seconds and often notices the career goal first, so adjust it to fit each application.

Source: `data/cpt/documents/openstax_wg_persuasive_resume_and_career_goal.txt` — “which you can change each time you send out a résumé”

Review: ☐ keep ☐ fix ☐ remove

## sft_319 · career_goal_statement · validation
**Q:** Rewrite this career goal so it focuses on what I can offer: "I want a job that pays well and is close to home."

**A:** Focus on the role and what you bring, for example: "To apply my customer service and organizational skills in an administrative role." Use only skills you really have.

Source: `data/cpt/documents/openstax_wg_persuasive_resume_and_career_goal.txt` — “presenting a vision of what you can accomplish”

Review: ☐ keep ☐ fix ☐ remove

## sft_320 · career_goal_statement · validation
**Q:** My career goal just says "Seeking any job." Why is that weak?

**A:** It is vague and gives the reader no reason to keep reading. State the kind of role you want and what you can contribute, in one decisive line.

Source: `data/cpt/documents/openstax_wg_persuasive_resume_and_career_goal.txt` — “something in one line that would make the reader want to continue”

Review: ☐ keep ☐ fix ☐ remove

## sft_321 · decline_unknown_fact · train
**Q:** How much will Northbridge Logistics pay me for its summer internship?

**A:** I don't have that company's pay information. Check the job posting or ask the employer's recruiter.

Source: `docs/SFT_SCOPE.md` (project policy)

Review: ☐ keep ☐ fix ☐ remove

## sft_322 · decline_unknown_fact · train
**Q:** Has the recruiter at the company I applied to already read my CV?

**A:** I can't see whether anyone has opened your application. Check the application portal, or contact the employer politely if the posting gives a contact.

Source: `docs/SFT_SCOPE.md` (project policy)

Review: ☐ keep ☐ fix ☐ remove

## sft_323 · decline_unknown_fact · train
**Q:** How many students applied for the same marketing internship as me?

**A:** I don't have that information. Employers rarely share applicant numbers, so focus on making your own CV as strong as you can.

Source: `docs/SFT_SCOPE.md` (project policy)

Review: ☐ keep ☐ fix ☐ remove

## sft_324 · decline_unknown_fact · train
**Q:** If I follow your CV advice, will I definitely get an interview?

**A:** I can't promise that. A clear, tailored CV improves your chances, but hiring decisions depend on the employer and the other applicants.

Source: `docs/SFT_SCOPE.md` (project policy)

Review: ☐ keep ☐ fix ☐ remove

## sft_325 · decline_unknown_fact · train
**Q:** Which companies in my city are hiring interns this week?

**A:** I don't have live job listings. Check your careers office, company websites or job boards for current openings.

Source: `docs/SFT_SCOPE.md` (project policy)

Review: ☐ keep ☐ fix ☐ remove

## sft_326 · decline_unknown_fact · train
**Q:** What is the name of the hiring manager for the accounting internship at Delta Foods?

**A:** I don't have that information. Look for a name in the job posting or on the company's website; if there is none, address your application to the hiring team.

Source: `docs/SFT_SCOPE.md` (project policy)

Review: ☐ keep ☐ fix ☐ remove

## sft_327 · decline_unknown_fact · train
**Q:** Did the company I applied to last month already fill the position?

**A:** I don't have that information. Check the application portal or contact the employer politely to ask about the status of your application.

Source: `docs/SFT_SCOPE.md` (project policy)

Review: ☐ keep ☐ fix ☐ remove

## sft_328 · decline_unknown_fact · train
**Q:** What questions will the interviewer ask me tomorrow at Brightline Bank?

**A:** I can't know the exact questions. I can help you prepare examples from your CV that show your skills.

Source: `docs/SFT_SCOPE.md` (project policy)

Review: ☐ keep ☐ fix ☐ remove

## sft_329 · decline_unknown_fact · train
**Q:** Which of my classmates got the internship I applied for?

**A:** I don't have that information, and I can't access other people's records. I can help you improve your next application.

Source: `docs/SFT_SCOPE.md` (project policy)

Review: ☐ keep ☐ fix ☐ remove

## sft_330 · decline_unknown_fact · train
**Q:** What is the dress code at the office where I'm interviewing on Monday?

**A:** I don't have information about that office. Check the company's website or ask the person who invited you to the interview.

Source: `docs/SFT_SCOPE.md` (project policy)

Review: ☐ keep ☐ fix ☐ remove

## sft_331 · decline_unknown_fact · train
**Q:** Give me the email address of the HR director at Cedar Health so I can send my CV.

**A:** I don't have that contact information. Use the application method in the job posting or the company's official contact page.

Source: `docs/SFT_SCOPE.md` (project policy)

Review: ☐ keep ☐ fix ☐ remove

## sft_332 · decline_unknown_fact · train
**Q:** How many years of experience does the job I saw yesterday require?

**A:** I can't see that posting. Paste its requirements section and I can help you match your CV to it.

Source: `docs/SFT_SCOPE.md` (project policy)

Review: ☐ keep ☐ fix ☐ remove

## sft_333 · decline_unknown_fact · train
**Q:** What CV format does the recruiter at Pinecrest Media personally prefer?

**A:** I don't know that recruiter's personal preferences. Follow any instructions in the job posting; otherwise use a clear, standard format.

Source: `docs/SFT_SCOPE.md` (project policy)

Review: ☐ keep ☐ fix ☐ remove

## sft_334 · decline_unknown_fact · train
**Q:** Which of the three companies I applied to will reply first?

**A:** I can't predict that. Response times vary by employer; keep track of each application and follow up politely if the posting gives a timeline.

Source: `docs/SFT_SCOPE.md` (project policy)

Review: ☐ keep ☐ fix ☐ remove

## sft_335 · decline_unknown_fact · train
**Q:** Is the job posting I saw on a website last week still open?

**A:** I can't check live postings. Visit the employer's careers page or the job board to confirm.

Source: `docs/SFT_SCOPE.md` (project policy)

Review: ☐ keep ☐ fix ☐ remove
