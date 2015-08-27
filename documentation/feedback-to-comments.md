# Feedback to comments

Our feedback to the jury comments we received on our [2015 GBIF Ebbe Nielsen Challenge - Round 1](http://devpost.com/software/gbif-dataset-metrics) submission:

## 1. Limitations of a Chrome extension

> The extension is for Chrome only, but Chrome accounts for about 50% of GBIF users. In addition, about half of the Chrome users had their language set to something other than English. Can this extension be extended further to reach a wider audience, either for other browsers or other languages?

This extension was developed as a proof of concept (for displaying dataset metrics) and we decided to implement it as a Chrome extension for two reasons: 1) it allows us to show metrics in context on the GBIF website (which makes for a better user experience) without us needing access to the GBIF servers, and 2) it allows our code to be portable, because Chrome extensions (in contrast with e.g. Firefox plugins) are written in HTML, CSS and Javascript, which are web technologies.

However, if this proof of concept proves useful, **we strongly believe its functionality should be implemented on the GBIF infrastructure**, to allow:

1. a uniform experience for all users, independent of their browser
2. faster rendering of the charts (since nothing needs to be injected after page load)
3. faster and more robust metrics calculation (e.g. on the Hadoop cluster) tied to the harvesting and indexing infrastructure, without the need to periodically download all GBIF datasets
4. metrics to be exposed via a dedicated API, so developers can build new tools upon these

Large parts of our proof of concept can be reused to implement this: 1) our frontend code is portable, and 2) we wrote [extensive documentation](../documentation) for all the features and their underlying business logic (i.e. how we calculate metrics), including the sections: "how we categorize", "suggestions for improvement", and "suggestions for GBIF (i.e. potential bugs)".

Our extension currently only supports English, as that is the only language currently supported by the GBIF portal.

## 2. Community

> The general approach of providing additional functionality on top of an existing web site is interesting. Related approaches include bookmarklets. Is there scope to create a library of code with documentation so that anyone could use it as the basis of creating their own extension? In other words, can we imagine a community of extensions/bookmarklets where people can enhance the GBIF portal (and hence perhaps nudge GBIF to include some of this functionality in future releases)?

This is an interesting approach, and would require: 1) a commitment from the GBIF team to keep the frontend stable (e.g. stable names for containers and classes, etc.), as extensions rely on those for inserting content, 2) documentation of the frontend, so developers know where to start, 3) boilerplate code for extensions so shared functionality between those does not have to be rewritten, 4) a platform to share development experience (i.e. GitHub), and 5) a platform where users can find extensions (e.g. on top of Chrome Web Store). This was beyond the scope of this challenge and should be developed in collaboration with GBIF.

The same is true for bookmarklets. We did not use a bookmarklet for this proof of concept, as those need to be executed by the user (on each page reload), while we wanted to provide a seamless integration of dataset metrics on each GBIF dataset page, without the need for user activation.

Another approach would be to open the GBIF frontend code to contributions via pull requests. This process would be somewhat slower (as it is tied to releases of the frontend) and does not allow users to customize their experience by installing specific extensions, but has all the advantages of not using extensions (see comment 1) and is thus more stable. As the GBIF frontend makes use of its own GBIF web services, no backend knowledge is required by frontend developers, making the learning curve easier. A known framework (e.g. Angular JS) and documentation are probably required too to allow for easier contributions. Another incentive would be to assign prize money/short term contracts to implement certain features.

## 3. On the fly metrics

> The participants suggest a couple of potential enhancements, among them the ability to produce “on the fly” metrics for search results. That would be an incredibly useful extension to prioritize. There are clearly performance concerns with generating statistics on the fly, so maybe this feature would only be available for queries that return a dataset under a certain size limit.

Yes, on the fly metrics would be very cool and useful, but are challenging to implement. We think the current proof of concept functionality (using pre-processed metrics) should be implemented on the GBIF infrastructure first (see comment 1), before this is tackled. And even on the GBIF infrastructure, on the fly metrics will probably have to be limited in scope.

## 4. Update strategy

> The approach of pre-processing each dataset’s statistics is clearly meant to improve performance and user experience. But with 12K+ datasets in an ongoing state of flux, keeping up with changes may be a challenge. How does the team plan to detect changes and update statistics. In the “limitations” section they only address how users can request updates to a specific dataset. Is it possible to develop an update strategy that, perhaps, would include automation of dataset refresh detection and updating of the statistics based on need or a prioritization scheme based on dataset size and popularity of use?

Yes, keeping the metrics up to date is a challenge and we currently do not have an update strategy, except for manually downloading all data from GBIF from time to time and processing these. We did not invest much in optimizing this harvesting process, as we consider the extension to be mainly a (frontend) proof of concept, which functionality should ideally be implemented on the GBIF infrastructure (see comment 1). Although the functionality is there, any backend code we wrote for harvesting and processing the datasets, will have to be reimplemented considerably on the GBIF infrastructure, which can then 1) make use of the harvesting and indexing infrastructure to be notified of dataset updates, 2) pre-process metrics on a dataset level, instead of doing so for all datasets, and 3) store those metrics and expose those via APIs to the frontend, instead of relying on a separate data store (such as our CartoDB).

Another case in point that this processing should be done more efficiently, tied more closely to GBIF's harvesting and indexing infrastructure, and on a larger infrastructure overall, is that we were not able to process all of GBIF’s data on our development infrastructure (i.e. a MacBook Pro), but had to rely on [Amazon EC2 infrastructure](https://aws.amazon.com/ec2/) to aggregate all metrics from the occurrences in a reasonable time span. Even then, downloading takes 0.5 days, extracting metrics 2 days, and aggregating (on EC2) a couple of hours.
