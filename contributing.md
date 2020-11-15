# Contributing

Anyone is welcome to contribute and create a pull request at will, however, we will instantly deny any pull request that does not meet these guidelines, we will **not** fix issues for you.
With that said, here's our list of guidelines.

# Standards
- Naming Conventions **must** be consistent with the naming conventions currently being used (`under_score` for methods and 'camelCase' for everything else)    
- No "bodge" code, by this we mean don't want workaround fixes, things should be done the proper way.
- Do not create "Spagetti Code" - i.e. writing so much code that it eventually causes a complete unorganised mess. To keep code clean, use the appropriate comment headers for what you're adjusting or adding if nessary.
- Please try to comment your code so that we can understand what different bits are doing

# Contributing
If you want to contribute please fork the most recent dev branch [not master] and create a pull request as soon as you can, make sure your fork is also kept up to date.
The master branch represents the code which is currently "live" - i.e. it's being run off of the host - the dev branches are the branches in active development.

**Do not** write or start any changes without raising an issue first. An issue allows us to define a priority, assign a target release and convert it into a task/peice of work that needs doing if approved. There is a chance the changes you want to make are not something that we either want or feel like needs doing, by not making changes before having explicit approval will save you time as you don't want to have written all the changes only to be told we don't want them. Pull Requests that do not have an associated issue will usually be closed on those grounds, small tweaks may be allowed, but we would prefer an issue be raised first.  

Make sure to follow the standards set out above when making your PR, we may make slight adjustments within your PR for you but in most cases we will just request changes from you. When making a PR please target the correct devlopment branch, this will be wilfred-**vvv** where **vvv** is the target release as set out in the issue/task that has been created. For example, Wilfred 370 would be branch wilfred-**370**. If you select the wrong branch we will close the PR and ask you to target the correct one.

Any pull requests must pass the automated tests, if they do not, they cannot be merged. If your PR fails the automated tests please figure out why and fix the issue, any PR that has been failing for a prolonged period of time with no action from the contributor will be closed.  

# Discord Rewards
Frequent contnributors will be given a contributor badge on your discord profile.

# Testing
Testing of the in-dev branch is ran on a twin server, contributors with the Contributor Rank will be invited to this server to help with testing. The contributor role on the test server will give admin like permissions with the bot, however, everything is runnong off a seperate database and won't affect the live server.

# Collaborators/Staff
Collaborators **should not** commit directly to any branches on this repository unless you're a approved developer (I.e. Matt)
**Do not under any circumstances commit to Master**

# Disclaimer
Having an accepted contribution to the bot does not by any means grant you partial ownership or rights to the bot. In addition approved contributions may be removed at any time by the discretion of the developer. 
