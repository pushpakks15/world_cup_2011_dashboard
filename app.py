import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import seaborn as sns

df=pd.read_csv('worldcup2011.csv')
st.set_page_config(layout='wide',page_title='ICC WORLD CUP 2011')


def match_summary(match):
    st.empty()
    temp_df = df[df['match_no'] == match]
    team1 = temp_df['Team'].unique().tolist()[0]
    team2 = temp_df['Team'].unique().tolist()[1]
    st.title(f'{team1} vs {team2}')
    st.header(f'Match number: {match}')

    st.subheader("1st INNINGS")
    col1,col2,col3=st.columns(3)
    with col2:
        st.markdown(f"## Batting team: {team1}")
    with col3:
        st.write(f'## Bowling team: {team2}')
    with col1:
        score_1 = temp_df[temp_df['Team'] == team1]['total'].sum()
        wickets_1 = temp_df[temp_df['Team'] == team1]['wicket'].sum()
        st.markdown(f'## Total Score: {score_1}/{wickets_1}')
    with col2:
        st.markdown("### Top batsmen")
        temp_df2 = temp_df.groupby(['Team', 'batsmen'])['runs'].sum().reset_index()
        top_batsmen = temp_df2[temp_df2['Team'] == team1].sort_values(by='runs', ascending=False).head(3)[
            ['batsmen', 'runs']].set_index('batsmen')
        top_batsmen.rename(columns={'runs': 'Runs'}, inplace=True)
        balls_faced = temp_df.groupby('batsmen')['ball'].count()
        final_df = top_batsmen.merge(balls_faced, how='inner', on='batsmen').rename(columns={'ball': 'balls faced'})
        st.dataframe(final_df)
    with col3:
        st.markdown("### Top bowlers")
        temp_df3 = temp_df.groupby(['Team', 'bowler'])['wicket'].sum().reset_index()
        top_bowlers = temp_df3[temp_df3['Team'] == team1].sort_values(by='wicket', ascending=False).head(3)[
            ['bowler', 'wicket']].set_index('bowler')
        temp_df4 = temp_df.groupby(['Team', 'bowler'])['runs'].sum().reset_index()
        runs_given = temp_df4[temp_df4['Team'] == team1][['bowler', 'runs']].set_index('bowler')
        final_df2 = top_bowlers.merge(runs_given, how='inner', on='bowler')
        st.dataframe(final_df2)


    st.subheader("2nd INNINGS")
    col4, col5, col6 = st.columns(3)
    with col5:
        st.markdown(f"## Batting team: {team2}")
    with col6:
        st.markdown(f'## Bowling team: {team1}')
    score_2 = temp_df[temp_df['Team'] == team2]['total'].sum()
    wickets_2 = temp_df[temp_df['Team'] == team2]['wicket'].sum()
    with col4:
        st.markdown(f'## Total Score: {score_2}/{wickets_2}')
    with col5:
        st.markdown("### Top batsmen")
        top_batsmen = temp_df2[temp_df2['Team'] == team2].sort_values(by='runs', ascending=False).head(3)[
            ['batsmen', 'runs']].set_index('batsmen')
        top_batsmen.rename(columns={'runs': 'Runs'}, inplace=True)
        balls_faced = temp_df.groupby('batsmen')['ball'].count()
        final_df = top_batsmen.merge(balls_faced, how='inner', on='batsmen').rename(columns={'ball': 'balls faced'})
        st.dataframe(final_df)
    with col6:
        st.markdown("### Top bowlers")
        temp_df3 = temp_df.groupby(['Team', 'bowler'])['wicket'].sum().reset_index()
        top_bowlers = temp_df3[temp_df3['Team'] == team2].sort_values(by='wicket', ascending=False).head(3)[
            ['bowler', 'wicket']].set_index('bowler')
        temp_df4 = temp_df.groupby(['Team', 'bowler'])['runs'].sum().reset_index()
        runs_given = temp_df4[temp_df4['Team'] == team2][['bowler', 'runs']].set_index('bowler')
        final_df2 = top_bowlers.merge(runs_given, how='inner', on='bowler')
        st.dataframe(final_df2)

    st.subheader("Match Result :")
    if score_1 < score_2:
        st.markdown(f'## {team2} won by {10 - wickets_2} wickets')
    elif score_1 > score_2:
        st.markdown(f'## {team1} won by {score_1 - score_2} runs')
    elif score_1 == score_2:
        st.markdown('## Match Tied')
    else:
        st.markdown('## No result')

    return 0


def batting_records():
    option=st.selectbox('Select one',['Top Batsmen with most runs','Most hundreds','Most fifties',
                               'Highest strike rate','Highest average','Highest Scores',
                                      'Most sixes','Most fours'])
    if option=='Top Batsmen with most runs':
        st.markdown("## Top 5 batsmen")
        a,b,c=st.columns(3)
        with b:
            st.image('images/dilshan.jpg')
            st.write("Tillakaratne Dilshan")
        with c:
            st.image('images/sachin.webp')
            st.write("Sachin Tendulkar")
        with a:
            most_runs = df.groupby('batsmen')['runs'].sum().sort_values(ascending=False).head(5).reset_index().set_index('batsmen')
            st.dataframe(most_runs)

    elif option=='Most hundreds':
        st.markdown('## Most number of hundreds')
        most_hundreds = df.groupby(['batsmen', 'match_no'])['runs'].sum().reset_index()
        hun=most_hundreds[most_hundreds['runs'] > 100]['batsmen'].value_counts().head(5)
        d,e,f=st.columns(3)
        with d:
            st.dataframe(hun)
        with e:
            st.image('images/abd.jpg')
            st.write('Ab de Villiers')
        with f:
            st.image('images/tharanga.jpg')
            st.write('Upul Tharanga')

    elif option=='Most fifties':
        st.markdown('## Most number of fifties')
        most_fifties = df.groupby(['batsmen', 'match_no'])['runs'].sum().reset_index()
        g,h,i=st.columns(3)
        with g:
            st.dataframe(most_fifties[(most_fifties['runs'] > 50) & (most_fifties['runs'] < 100)]['batsmen'].value_counts().head(5))
        with h:
            st.image('images/Jonathan-Trott-England-007.webp')
            st.write('Jonathan Trott')
        with i:
            st.image('images/haddin.webp')
            st.write('Brad Haddin')

    elif option=='Highest strike rate':
        st.markdown('## Best strike rate')
        runs = df.groupby('batsmen')['runs'].sum().reset_index()
        balls = df.groupby('batsmen')['ball'].count().reset_index()
        balls_2 = balls[balls['ball'] > 100]
        strike_rate = runs.merge(balls_2, on='batsmen')
        strike_rate['SR'] = (strike_rate['runs'] / strike_rate['ball']) * 100
        j,k,l=st.columns(3)
        with j:
            st.dataframe(strike_rate.sort_values(by='SR', ascending=False).head(5).set_index('batsmen'))
        with k:
            st.image('images/polly.webp')
            st.write('Kieron Pollard')
        with l:
            st.image('images/kevin.jpg')
            st.write("Kevin O'Brien")

    elif option=='Highest average':
        st.markdown('## Best Average')
        runs = df.groupby('batsmen')['runs'].sum().reset_index()
        runs_2 = runs[runs['runs'] > 100]
        wickets = df.groupby('batsmen')['wicket'].sum().reset_index()
        avg = runs_2.merge(wickets, on='batsmen')
        avg['AVG'] = round(avg['runs'] / avg['wicket'], 2)
        m,n,o=st.columns(3)
        with m:
            st.dataframe(avg.sort_values(by='AVG', ascending=False).head(5).set_index('batsmen'))
        with n:
            st.image('images/abd2.webp')
            st.write('Ab de Villiers')
        with o:
            st.image('images/sanga.jpg')
            st.write('Kumar Sangakkara')

    elif option=='Highest Scores':
        st.markdown('## Highest scores')
        most_hundreds = df.groupby(['batsmen', 'match_no'])['runs'].sum().reset_index()
        p,q,r=st.columns(3)
        with p:
            st.dataframe(most_hundreds[most_hundreds['runs'] > 100][['batsmen', 'runs']].sort_values(by='runs', ascending=False).head(
             5).set_index('batsmen'))
        with q:
            st.image('images/sehwag.webp')
            st.write("Virender Sehwag")
        with r:
            st.image('images/England-Andrew-Strauss-Wo-007.webp')
            st.write('Andrew Strass')

    elif option=='Most sixes':
        st.markdown('## Most sixes')
        sixes = df[df['runs'] == 6].groupby('batsmen')['runs'].count().sort_values(ascending=False).head(5)
        s,t,u=st.columns(3)
        with s:
            st.dataframe(sixes)
        with t:
            st.image('images/ross.webp')
            st.write('Ross Taylor')
        with u:
            st.image('images/polly_ssix.webp')
            st.write('Kieron Pollard')

    elif option == 'Most fours':
        st.markdown('## Most fours')
        fours = df[df['runs'] == 4].groupby('batsmen')['runs'].count().sort_values(ascending=False).head(5)
        v,w,x=st.columns(3)
        with v:
            st.dataframe(fours)
        with w:
            st.image('images/dil_four.webp')
            st.write("Tillakaratne Dilshan")
        with x:
            st.image('images/tharanga_fours.jpg')
            st.write('Upul Tharanga')

def bowling_records():
    option=st.selectbox('Select one option',['Top wicket takers','Best Economy','Best figures'])
    if option=='Top wicket takers':
        st.markdown("## Most Wickets")
        most_wickets=df.groupby('bowler')['wicket'].sum().sort_values(ascending=False).head(5)
        a1,a2,a3=st.columns(3)
        with a1:
            st.dataframe(most_wickets)
        with a2:
            st.image('images/zak.jpg')
            st.write('Zaheer Khan')
        with a3:
            st.image('images/afridi.webp')
            st.write('Shahid Afridi')

    elif option=='Best Economy':
        st.markdown('## Best Economy')
        runs_given=df.groupby('bowler')['runs'].sum().reset_index()
        balls_bowled=df.groupby('bowler')['ball'].count().reset_index()
        economy=runs_given.merge(balls_bowled,on='bowler')
        economy['overs_bowled']=round(economy['ball']/6)
        economy['economy']=round(economy['runs']/economy['overs_bowled'],2)
        b1,b2,b3=st.columns(3)
        with b1:
            st.dataframe(economy[economy['overs_bowled']>20].sort_values(by="economy").head(5)[['bowler','economy']].set_index('bowler'))
        with b2:
            st.image('images/Saeed-Ajmal.jpeg')
            st.write('Saeed Ajmal')
        with b3:
            st.image('images/mendis.jpg')
            st.write('Ajanta Mendis')

    elif option == 'Best figures':
        st.markdown('## Best Bowling')
        runs_given=df.groupby(['bowler','match_no'])['runs'].sum().reset_index()
        best_b=df.groupby(['bowler','match_no'])['wicket'].sum().sort_values(ascending=False).reset_index()
        best_fig=best_b.merge(runs_given,on='bowler').sort_values(by=['wicket','runs'],ascending=False)[['bowler','wicket','runs']].drop_duplicates(subset=['bowler']).head(5)
        c1,c2,c3=st.columns(3)
        with c1:
            st.dataframe(best_fig.set_index('bowler'))
        with c2:
            st.image('images/malinga.webp')
            st.write('Lasith Malinga')
        with c3:
            st.image('images/afridi.webp')
            st.write('Shahid Afridi')


def team_records(team):
    a1,a2=st.columns(2)
    with a1:
        total = df.groupby(['Team', 'match_no'])['runs'].sum().reset_index()
        highest_score = total[total['Team'] == team].sort_values(by='runs', ascending=False).head(1)
        wickets = df.groupby(['Team', 'match_no'])['wicket'].sum().reset_index()
        final_df = highest_score.merge(wickets, on='match_no').head(2)
        lst = final_df['Team_y'].tolist()
        lst.remove(team)
        runs = final_df['runs'][0]
        wickets = final_df['wicket'][0]
        vs = lst[0]
        st.metric('### Highest Team Total',f'{runs}/{wickets} vs {vs}')

        st.markdown(f'#### Best batsman of {team}')
        most_runs = df[df['Team'] == team].groupby('batsmen')['runs'].sum().sort_values(ascending=False).head(
            1).reset_index().set_index('batsmen')
        st.dataframe(most_runs)
        if team == "India":
            st.image('images/sachin.webp')
        elif team == 'Sri Lanka':
            st.image('images/dilshan.jpg')
        elif team == 'Pakistan':
            st.image('images/misbah.webp')
        elif team == 'New Zealand':
            st.image('images/ross.webp')
        elif team == 'England':
            st.image('images/Jonathan-Trott-England-007.webp')
        elif team == 'South Africa':
            st.image('images/abd2.webp')
        elif team == 'Australia':
            st.image('images/haddin.webp')
        elif team == 'West Indies':
            st.image('images/smith.webp')
        elif team == 'Zimbabwe':
            st.image('images/ervine.png')
        elif team == 'Bangladesh':
            st.image('images/Imrul-Kayes-Bangladesh-007.jpg')
        elif team == 'Netherlands':
            st.image('images/doeschate2.webp')
        elif team == 'Ireland':
            st.image('images/neilobrien.png')
        elif team == 'Canada':
            st.image('images/bagai.jpg')
        else:
            st.image('images/obuya.webp')


    with a2:
        lowest_score = total[total['Team'] == team].sort_values(by='runs').head(1)
        wickets = df.groupby(['Team', 'match_no'])['wicket'].sum().reset_index()
        final_df_2 = lowest_score.merge(wickets, on='match_no').head(2)
        lst2 = final_df_2['Team_y'].tolist()
        lst2.remove(team)
        runs = final_df_2['runs'][0]
        wickets = final_df_2['wicket'][0]
        vs = lst2[0]
        st.metric('### Lowest Team Total',f'{runs}/{wickets} vs {vs}')
        st.markdown(f'#### Best Bowler of {team}')
        most_wickets = df.groupby('bowler')['wicket'].sum().sort_values(ascending=False).reset_index()
        if team == "India":
            st.dataframe(most_wickets.iloc[0])
            st.image('images/zak.jpg')
        elif team == 'Sri Lanka':
            st.dataframe(most_wickets.iloc[4])
            st.image('images/murali.jpg')
        elif team == 'Pakistan':
            st.dataframe(most_wickets.iloc[1])
            st.image('images/afridi.webp')
        elif team == 'New Zealand':
            st.dataframe(most_wickets.iloc[2])
            st.image('images/southee.jpg')
        elif team == 'England':
            st.dataframe(most_wickets.iloc[13])
            st.image('images/swann.webp')
        elif team == 'South Africa':
            st.dataframe(most_wickets.iloc[3])
            st.image('images/peterson.jpg')
        elif team == 'Australia':
            st.dataframe(most_wickets.iloc[14])
            st.image('images/Brett-Lee.webp')
        elif team == 'West Indies':
            st.dataframe(most_wickets.iloc[8])
            st.image('images/roach.webp')
        elif team == 'Zimbabwe':
            st.dataframe(most_wickets.iloc[21])
            st.image('images/price.webp')
        elif team == 'Bangladesh':
            st.dataframe(most_wickets.iloc[20])
            st.image('images/shakib.webp')
        elif team == 'Netherlands':
            st.dataframe(most_wickets.iloc[32])
            st.image('images/seelar.webp')
        elif team == 'Ireland':
            st.dataframe(most_wickets.iloc[19])
            st.image('images/mooney.jpg')
        elif team == 'Canada':
            st.dataframe(most_wickets.iloc[10])
            st.image('images/baidwan.jpg')
        else:
            data = {'bowler': ['Thomas Odoyo'],
                    'wickets': [8]}
            kenya = pd.DataFrame(data).set_index('bowler')
            st.dataframe(kenya)
            st.image('images/odoyu.webp')

    if team == "India":
        st.write("India had an impressive run in the tournament, reaching the final. They finished at the top of Group B, winning all their group stage matches except for a tie against England. In the knockout stages, India defeated Australia in the quarterfinal and arch-rivals Pakistan in the semifinal. In the final, held at Wankhede Stadium in Mumbai, India faced Sri Lanka and won the match by 6 wickets. India's key players included Sachin Tendulkar, Virender Sehwag, Yuvraj Singh, and MS Dhoni.")
        st.markdown(f'## Key moments of India in World Cup')
        st.write("Virender Sehwag's explosive 175 against Bangladesh in the opening match set the tone for India's campaign.")
        st.image('images/sehwag175.jpg')
        st.write('The thrilling tie between India and England in the group stage.')
        st.image('images/ind_vs_eng_tie.jpg')
        st.write("Yuvraj Singh's all-round performances, scoring crucial runs and taking wickets consistently for India.")
        st.image('images/2011-wc-yuvraj-singh.jpg')
        st.write("Ms Dhoni's last ball six in the finals to lead India to their second world cup win.")
        st.image('images/last_ball_six.jpg')
        st.write('India wins the World cup after 28 years...')
        st.image('images/world cup win.jpeg')
    elif team == 'Sri Lanka':
        st.write("Sri Lanka also had a strong performance throughout the tournament. They finished second in Group A, losing just one match to Pakistan. In the quarterfinals, they defeated England comfortably. In the semifinal, they defeated New Zealand to reach the final against India. In the final, they posted a competitive total but couldn't defend it, finishing as runners-up.")
        st.markdown(f'## Key moments of Sri Lanka in World Cup')
        st.write("Tillakaratne Dilshan's consistent performances with the bat, including his brilliant century against Zimbabwe in the group stage, were crucial for Sri Lanka's success.")
        st.image('images/dilshan500.jpg')
        st.write("Mahela Jayawardene's epic century in the finals")
        st.image('images/jaywardahane.webp')
    elif team == 'Pakistan':
        st.write('Pakistan performed well in the group stage, finishing as Group A leaders, winning all their matches except for a no-result against Sri Lanka. In the quarterfinal, they faced the West Indies and won convincingly. However, their journey came to an end in the semifinal when they were defeated by India.')
        st.markdown(f'## Key moments of Pakistan in World Cup')
        st.write("Shahid Afridi's impressive 5-wicket haul against Kenya took place during the ICC Cricket World Cup 2011. The match occurred on February 23, 2011, at the Mahinda Rajapaksa International Stadium in Hambantota, Sri Lanka.")
        st.image('images/afridi5fer.png')
        st.write("The semifinal against India was a crucial match for Pakistan, but they couldn't get past their arch-rivals to reach the final.")
        st.image('images/India-Pakistan_2011.webp')
    elif team == 'New Zealand':
        st.write('New Zealand finished third in Group A. They had a thrilling win against Pakistan but suffered a defeat against Sri Lanka. In the quarterfinals, they beat South Africa in a tight match but were eliminated by Sri Lanka in the semifinals.')
        st.markdown(f'## Key moments of New Zealand in World Cup')
        st.write("Ross Taylor's century against Pakistan in the group stage was an exceptional innings.")
        st.image('images/taylorvspak.webp')
        st.write("The quarterfinal against South Africa, where New Zealand's victory in the Super Over took them to the semifinals.")
        st.image('images/savsnz.jpg')
    elif team == 'England':
        st.write("England finished third in Group B, losing to Ireland and Bangladesh. In the quarterfinals, they faced Sri Lanka and were defeated, ending their World Cup campaign.")
        st.markdown(f'## Key moments of England in World Cup')
        st.image('images/engvsire.jpg')
        st.image('images/engvsban.jpg')
        st.write("England's unexpected loss to Ireland and Bangladesh")
        st.image('images/engvssl.webp')
        st.write("England's loss to Sri Lanka in the quarterfinals.")
    elif team == 'South Africa':
        st.write("South Africa had a strong showing in the group stage, finishing second in Group B, losing only to England. However, their infamous quarterfinal against New Zealand was a nail-biter, ending in a tie. In the Super Over, they faltered, resulting in their elimination.")
        st.markdown(f'## Key moments of South Africa in World Cup')
        st.write("Consistent and Brilliant batting of Ab de Villiers throughout the world cup")
        st.image('images/abd3.jpg')
        st.write('Defeated India in the group stages')
        st.image('images/savsind.jpg')
        st.write('Got defeated by New Zealand in a thriller')
        st.image('images/savsnz2.webp')
    elif team == 'Australia':
        st.write(
            "Australia, the defending champions, had a mixed run in the tournament. They finished second in Group A, behind Pakistan. In the quarterfinals, they suffered a surprising defeat to India and were knocked out of the tournament.")
        st.markdown(f'## Key moments of Australia in World Cup')
        st.write("Australia's thrilling match against Kenya in the group stage, where Brett Lee's five-wicket haul helped them defend a modest total.")
        st.image('images/ausken.webp')
        st.write(" Ricky Ponting's century against India in the group stage was an excellent display of batting.")
        st.image('images/ponting_century.png')
        st.write("Brett Lee's fiery spell of 4/28 against Pakistan")
        st.image('images/Brett-Lee4w.png')
        st.write("The quarterfinal clash against India, where Australia's defeat marked the end of their dominance in the World Cup.")
        st.image('images/indvsaus.webp')
    elif team == 'West Indies':
        st.write("West Indies finished fourth in Group B, which included a notable win against Bangladesh. In the quarterfinal, they faced Pakistan but couldn't progress further.")
        st.markdown(f'## Key moments of West Indies in World Cup')
        st.write("Kieron Pollard's blistering 94 against India in the group stage.")
        st.image('images/pollyvsind.webp')
        st.write("Kemar Roach's 6/27 against the Netherlands in the group stage.")
        st.image('images/West-Indies-Kemar-Roach--007.webp')
    elif team == 'Zimbabwe':
        st.write("Zimbabwe finished sixth in Group A and couldn't progress to the quarterfinals.")
        st.markdown(f'## Key moments of Zimbabwe in World Cup')
        st.write("Sean Williams' century against the West Indies in the group stage.")
        st.image('images/seanwilliams.jpg')
    elif team == 'Bangladesh':
        st.write("Bangladesh finished fifth in Group B, showing promising performances but failing to reach the knockout stages.")
        st.markdown(f'## Key moments of Bangladesh in World Cup')
        a,b=st.columns(2)
        with a:
            st.write("Shafiful islam's brilliant bowling against Ireland")
            st.image('images/Shafiul-Islam-v-IRE.webp')
        with b:
            st.write("Bangladesh's historic win over England in the group stage.")
            st.image('images/banrunchase.webp')
    elif team == 'Netherlands':
        st.write("Netherlands finished last in Group B and couldn't make it to the knockout stages.")
        st.markdown(f'## Key moments of Netherlands in World Cup')
        st.write("Ryan ten Doeschate's impressive all-round performances.")
        st.image('images/ryanbat.jpg')
        st.image('images/ryanball.webp')
    elif team == 'Ireland':
        st.write("Ireland had a remarkable run, finishing third in Group B. They caused one of the biggest upsets of the tournament by defeating England in the group stage. Despite their impressive efforts, they couldn't make it to the knockout stages.")
        st.markdown(f'## Key moments of Ireland in World Cup')
        st.write("Kevin O'Brien's stunning century against England, leading Ireland to a remarkable victory in the group stage.")
        st.image('images/kob.jpg')
    elif team == 'Canada':
        st.write("Canada finished last in Group A and couldn't advance to the quarterfinals.")
        st.markdown(f'## Key moments of Canada in World Cup')
        st.write("Hiral Patel's 54 runs against Australia in the group stage.")
        st.image('images/hiral.webp')
    else:
        st.write("Kenya struggled in the tournament and finished last in Group A, failing to qualify for the knockout stages.")
        st.markdown(f'## Key moments of Kenya in World Cup')
        st.write("Collins Obuya's 98 against Australia in the group stage.")
        st.image('images/obuyavsaus.jpg')


def load_overall_analysis():
    st.markdown("## Overall in the ICC Cricket World Cup 2011 tournament...")
    c1,c2,c3,c4=st.columns(4)
    with c1:
        st.metric('Total no. of players participated',len(df.batsmen.unique()))
        st.metric('Total sixes', df[df['runs'] == 6].runs.count())
        st.metric('Total catches', df[df['kind'] == 'caught']['kind'].count())
    with c2:
        st.metric('Total runs scored',df.total.sum())
        st.metric('Total fours', df[df['runs'] == 4].runs.count())
        st.metric('Total LBWs', df[df['kind'] == 'lbw']['kind'].count())
    with c3:
        st.metric("Total balls bowled",df.ball.count())
        total_centuries = df.groupby(['match_no', 'batsmen'])['runs'].sum().reset_index()
        st.metric('Total centuries', total_centuries[total_centuries['runs'] > 100].runs.count())
        st.metric("Total bowled wickets", df[df['kind'] == 'bowled']['kind'].count())
    with c4:
        st.metric('Total wickets taken',df.wicket.sum())
        total_centuries = df.groupby(['match_no', 'batsmen'])['runs'].sum().reset_index()
        st.metric('Total fifties',
                  total_centuries[(total_centuries['runs'] > 50) & (total_centuries['runs'] < 100)].runs.count())
        st.metric("Total run-outs", df[df['kind'] == 'run out']['kind'].count())

    # Top 3 highest partnerships
    z1,z2=st.columns(2)
    with z1:
        st.markdown('## Top 3 highest partnerships')
        df2 = df.groupby(['batsmen', 'non_striker', 'match_no']).runs.sum().sort_values(ascending=False).head(
            5).reset_index().set_index('runs').drop_duplicates(subset=['match_no'])
        st.dataframe(df2)
        st.image('images/sapartenership.webp')
    with z2:
        st.image('images/partnership.webp')
    temp_df = df.sort_values(by='match_no')
    temp_df_2 = temp_df.groupby('match_no')['runs'].sum().reset_index()
    st.markdown('## Trends of runs scored from first to last matches')
    st.pyplot(sns.lineplot(data=temp_df_2, x='match_no', y='runs').figure)
    st.markdown('## Most balls bowled')
    temp_df_3 = df.groupby('bowler')['ball'].count().sort_values(ascending=False).head(5).reset_index()
    st.pyplot(sns.barplot(data=temp_df_3, x='bowler', y='ball').figure)





def homepage():
    st.write("Welcome to the homepage!")
    st.image('images/logo.png')
    st.title('ICC CRICKET WORLD CUP 2011')
    st.write('The 2011 ICC Cricket World Cup was the tenth Cricket World Cup. It was played in India, Sri Lanka, and for the first time in Bangladesh.')
    st.markdown('### **Champion:** [India](https://www.google.com/search?rlz=1C1ONGR_enIN1017IN1017&q=India+national+cricket+team&si=ACFMAn_Gd9OM2CPb2aZmeZqmDNcQe6dffWLqUS3eIZkPr91_p1wUiwd7EVIwswUlEm-Wn8PR6q4eni-m-eSxPZvXGMSDdOOtJd88rmhHm6F-iXMfn5RRc8gDzl-tzGoRjpUA4eO4ESgWnMg2zFwNZkbSCatiEdGHjPeTGpWB_p3ULGgpVSw8b0qu3132lwAyHZjeL_HzufF1tiMJ_m3sEP0G4fOh-88raA%3D%3D&sa=X&ved=2ahUKEwiamaS4qamAAxVmg2MGHeuyC4oQmxMoAXoECEAQAw&biw=1536&bih=707&dpr=1.25)')
    st.markdown('### **Dates: 19 Feb 2011 – 2 Apr 2011**')
    st.markdown('### **Most runs: [Tillakaratne Dilshan](https://www.google.com/search?sa=X&bih=707&biw=1536&rlz=1C1ONGR_enIN1017IN1017&hl=en&q=Tillakaratne+Dilshan+(500)&stick=H4sIAAAAAAAAAONgVuLUz9U3MM7NNstZxCoVkpmTk5idWJRYkpeq4JKZU5yRmKegYWpgoAkA9SuftCoAAAA&ved=2ahUKEwjx-YLStKmAAxVB9zgGHUTZD4oQmxMoAXoECEEQAw) (500)**')
    st.markdown('### **Host(s): India; Sri Lanka; Bangladesh**')
    st.markdown('### **Player of the series: [Yuvraj Singh](https://www.google.com/search?sa=X&bih=707&biw=1536&rlz=1C1ONGR_enIN1017IN1017&hl=en&q=Yuvraj+Singh&stick=H4sIAAAAAAAAAONgVuLUz9U3MLLIyS5axMoTWVpWlJilEJyZl54BAO3HXRAcAAAA&ved=2ahUKEwjx-YLStKmAAxVB9zgGHUTZD4oQmxMoAXoECEwQAw)**')
    st.video('De Ghumake - The Official ICC Cricket WC 2011 Anthem _ HQ.mp4')

def main():
    st.sidebar.title('RECORDS')
    option = st.sidebar.selectbox('Select one', ['Home', 'MATCHES','BATTING RECORDS', 'BOWLING RECORDS', 'TEAM RECORDS','OVERALL ANALYSIS'])

    if option == 'Home':
        homepage()


    elif option == 'MATCHES':
        st.write("Select a match number from the sidebar to see the match summary.")

        match = st.sidebar.selectbox('Select match number', range(1, 50))
        btn1 = st.sidebar.button("Fetch match summary")

        if btn1:
            match_summary(match)

    elif option == 'BATTING RECORDS':
        batting_records()

    elif option == 'BOWLING RECORDS':
        bowling_records()

    elif option == 'TEAM RECORDS':
        team=st.sidebar.selectbox("Select one Team",df.Team.unique())
        team_records(team)

    else:
        load_overall_analysis()

if __name__ == "__main__":
    main()