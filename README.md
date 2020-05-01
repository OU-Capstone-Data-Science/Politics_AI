# Vision Document

Poli-Tech AI Capstone Project

## Revision History
| Date     | Revision | Description         | Author                          |
| -------- | -------- | ------------------- | ------------------------------- |
| mm/dd/yy | x.x      | Version Description | Name(s)                         |
| 04/30/20 | 0.1      | Initial version     | Jacob, David, Alex, Eric        |

### **Table of Contents**
1. Introduction
	* Purpose
	* Solution Overview
	* References
2. User Description
	* User/Market Demographics
	* User Personas
	* User Environment
	* Key User Needs
	* Alternatives and Competition
3. Stakeholders
    * Users/Investors
4. Product Overview
	* Product Perspective
	* Product Position Statement
	* Summary of Capabilities
	* Assumptions and Dependencies
5. Product Features
	* Live Sentiment Analysis
	* Polling Data
	* Twitter Metrics
	* Candidate Information and Policies
	* Sentiment Analysis Over Time
6. Exemplary Use Cases
    * Researching Candidates on Social Media
7. Nonfunctional Requirements
	* Usability
	* Reliability
	* Performance 
8. Documentation Requirements
	* README File
	* Testing File
	* Deployment File
9.  Table of Acronyms and Abbreviations

## Introduction
* Purpose
	* This capstone project tackels a very important issue; the American people are under-informed about government and politics. When it is time for an election, media sources contradict each other, politicians contradict each other, and the American people form their political opinions based around their lifestyle and personal values. Everyone's vote counts the same, and unless the American people begin to do more political research, votes will be cast in ways that may contradict the individual's beliefs, or votes may not be cast at all.

* Solution Overview
	* Our capstone provides tools to help the American people learn more about active political candidates in an easy and fun way. Our project is a deployment of a webapp within a website (listed as <www.politech.xyz>). This webapp has 5 unique tabs, and each tab helps provide different insight into the politcal spectrum revolving around presidential candidates and social media.

* References
	* Chris Tse is our Product Owner and Dr. Rafal Jabrzemski is our Software Engineering instructor.

## User Description
* User/Market Demographics
	* The total population of the United States in 2014 was about 314.1 million. Approximately 86.9% of the population was native-born citizens, 6% were naturalized, and 7.1% were non-citizens. All Americans are potential users for our product.

* User Personas
	* White/European/Middle Eastern American
	* African American
	* Native American/Alaska Native
	* Asian American
	* Native Hawaiian/Pacific Islander

* User Environment
	* A smart device or computer that has internet access. The ideal user environment would be a laptop or desktop computer.

* Key User Needs
	* Technolocy capable of internet access, a basic understanding of twitter, a basic understanding of American politics.

* Alternatives and Competition
	* <www.270towin.com>
	* <2020campaigntracker.com>
	* <www.pbslearningmedia.org/collection/election-collection>

## Stakeholders
* Users/Investors
	* We currently don't have any stakeholders.

## Product Overview
* Product Perspective
	* Because our product has the potential to have concurrant users, this perspective is best described as a multiuser product perspective. The user community will most likely be people who are active on twitter and enjoy stating their political opinions. They would be able to see the same information in real time, and discuss their individual differences more clearly while using our product. It will be much more difficult for the user community to have information bias while collaborating with our product.

* Product Position Statement
	* Our product offers opinion information and factual information in visual and text-based formats. This product lets those who like to read campaign policy details to do so, while also letting those who are not as politically inclined or who are visual learners to easily interpret our graphed data. By providing different styles of learning in one application, we expand our consumer base and provide a better overall user experience.

* Summary of Capabilities
	* Our product is capable of providing sentiment visualization of tweets from twitter in both real time and from the past. It also provides polling statistics, tweet statistics, and candidate information from wikipedia.

* Assumptions and Dependencies
	* This product is provided in English only, but tweets may be written in other languages. There are no accomodations in place for people with physical disabilites such as vision loss. Due to vulgar language that can be posted on twitter, this product may not be suitable for children.

## Product Features
1. Live Sentiment Analysis
   * The components of this tab from top to bottom are a search box, a line graph, and a twitter feed column. A word or phrase in the search box is used to display tweets in the twitter feed, the tweet sentiment value beside the tweet, and the tweet sentiment value on the line graph. The tweets come from twitter in real time, and the contents of the search box can be changed. This allows users to see how the twitter community feels about certain topics by filtering tweets by that topic.
   
2. Polling Data
   * This tab consists of a static multi-line graph. This graph represents the poll data for the top two contending 2020 Democratic Presidential candidates (Joe Biden and Bernie Sanders). The included poll data ranges from the beginning on 2019 to February of 2020.
   
3. Twitter Metrics
   * This tab contains an interactive bar graph. The data the bar graph contains can be filtered with 3 interactive drop-down boxes. The first box lets you choose between all candidates or active candidates. The second box lets you selected or deselect candidates to be included in the graph. The third box lets you choose the specific twitter metric for which the candidates will be compared. The included metric options are average favorites per tweet, average retweets per tweet, and average tweets per day. By comparing several candidates at once, users can see how active the candidates are on twitter. Users can also infer how twitter users feel about the candidates based on retweet and favorite averages.
   
4. Candidate Information and Policies
   * This tab contains 3 interactive drop-down boxes and a content view window. The drop down boxes filter for specific candidate policy topics, and the content view window shows the information on the current policy topic found on wikipedia. The first drop down box lets you choose between all candidates or active candidates. The second box lets you choose a specific candidate. The third box lets you choose a policy topic. By providing factual information about candidates and their policy, users can actively research the candidates to help them have more informed political opinions.

5. Sentiment Analysis Over Time
   * This tab contains 2 interactive drop-down boxes and a  multi-line graph. The two drop-down boxes filter which candidate information is displayed in the multi-line graph. The multi-line graph shows the average tweet sentiment of the selected candidates over the past several months. By selecting multiple candidates, users can visually interpret the average social media sentiments of candidates over time, and infer how current events at specific times led to those average tweet sentiments. Users can also infer the general positivity/negativity of candidate social media presence as a whole.

## Exemplary Use Cases
> It's 2020, and the United States presidential primaries have begun. The primary Republican cadidate is Trump, with no questions asked, but there is no clear Democratic candidate in the beginning. As a college student, you are busy trying to keep your grades up in your classes, and you know you want to research all of the candidates, but you don't know how to research them quickly, in your spare time. Your friend tells you to go to the Politech website, so late one Thursday evening, you visit the website. After looking at all the tabs, you go back to the Twitter Metrics tab, and you are trying to learn whether Elizabeth Warren is active on Twitter. After comparing Elizabeth Warren to Bernie Sanders on this tab, you find out that she is active, in fact, more active than Bernie Sanders! Although, she does not get as many favorites or retweets as Bernie Sanders. Going to the "Candidate Information and Policies" tab, you begin to look at Elizabeth Warren's campaign information. You learned that she has been pushing to lower the interest rates on student loans, which is an important factor to you. You also learned that in 2018 she sent a letter to the United States Secretary of Veteran Affairs calling for the Veterans Affairs Department to release inspection reports. It seems like she is trying to improve the quality of live for veterans in nursing homes, which is another important factor to you. You are out of time for research tonight, but you are content with the knowledge you gained and will use Politech in the near future for more candidate research.

## Nonfunctional Requirements
* Usability
	* Learnability of this product is good because of common UI components and the use of common language. Efficiency of this product is good because the platform is the internet and the UI delay is minimal. Memorability is good because the product shows unique graphs, engages users with interactive drop-down boxes, and provides color-association.

* Reliability
	* This product's reliability is dependent on the user's internet connection and the state of the Google Cloud server.

* Performance
	* This product has good performance because the GCP VM product implementation is designed to minimize computational costs of the local database used to temporarily store live tweets. Currently this product has not been tested for performance with more than a few concurrent users.

## Documentation Requirements
* README File
	* The Vision Document (this file), which explains what Politech is all about.

* Testing File
	* Testing.md, located in the 'documentation' directory. This file explains the proposed testing procedure for this product.
  
* Deployment File
    * Deployment.md, located in the 'documentation' directory. This file explains how to deploy this product in a usable state for the end user.
	
## Table of Acronyms and Abbreviations
| Term     | Definition | 
| -------- | ---------- |
| GCP | Google Cloud Platform |
| UI | User Interface |
| VM | Virtual Machine |