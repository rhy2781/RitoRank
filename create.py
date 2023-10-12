import boto3;
import os;

CLIENT = boto3.client("athena")
RESULT_OUTPUT_LOCATION = os.environ.get("S3")

# Generate table for Game Data
def generateGamesTable():
    response = CLIENT.start_query_execution(
        QueryString="""
            CREATE EXTERNAL TABLE lol.`games`(
            `eventtime` string,
            `eventtype` string,
            `platformgameid` string,
            `participants` array<struct<keystoneid:bigint,hashedip:string,teamid:bigint,participantid:bigint,championname:string,accountid:bigint,abgroup:string,perks:array<struct<perkids:array<int>,perkstyle:bigint,perksubstyle:bigint>>,summonername:string,summonerlevel:bigint,magicpenetrationpercent:bigint,primaryabilityresource:bigint,cooldownreduction:bigint,spellvamp:bigint,lifesteal:bigint,magicpenetrationpercentbonus:bigint,magicpenetration:bigint,primaryabilityresourceregen:bigint,healthmax:bigint,position:struct<z:bigint,x:bigint>,magicresist:bigint,primaryabilityresourcemax:bigint,armorpenetrationpercentbonus:bigint,armorpenetrationpercent:bigint,attackdamage:bigint,ccreduction:bigint,currentgold:bigint,healthregen:bigint,attackspeed:bigint,xp:bigint,armor:bigint,level:bigint,armorpenetration:bigint,totalgold:bigint,health:bigint,abilitypower:bigint,stats:array<struct<value:float,name:string>>,goldpersecond:bigint>>,
            `sequenceindex` bigint,
            `assistants` array<int>,
            `monstertype` string,
            `killer` int,
            `inenemyjungle` boolean,
            `killerteamid` int,
            `localgold` int,
            `globalgold` int,
            `bountygold` int,
            `killtype` string,
            `stageid` int,
            `killergold` int,
            `dragontype` string,
            `gamename` string,
            `gameversion` string,
            `statsupdateinterval` bigint,
            `playbackid` bigint,
            `gametime` bigint,
            `nextdragonspawntime` bigint,
            `nextdragonname` string,
            `gameover` boolean,
            `teams` array<struct<inhibkills:bigint,towerkills:bigint,teamid:bigint,baronkills:bigint,dragonkills:bigint,assists:bigint,championskills:bigint,totalgold:bigint,deaths:bigint>>,
            `itemid` bigint,
            `participantid` bigint,
            `goldgain` bigint,
            `itemafterundo` bigint,
            `itembeforeundo` bigint,
            `skillslot` bigint,
            `participant` bigint,
            `evolved` boolean,
            `wardtype` string,
            `position` struct<z:bigint,x:bigint>,
            `placer` bigint)
            ROW FORMAT SERDE
            'org.openx.data.jsonserde.JsonSerDe'
            WITH SERDEPROPERTIES (
            'paths'='eventTime,eventType,evolved,gameName,gameOver,gameTime,gameVersion,goldGain,itemAfterUndo,itemBeforeUndo,itemID,nextDragonName,nextDragonSpawnTime,participant,participantID,participants,placer,platformGameId,playbackID,position,sequenceIndex,skillSlot,statsUpdateInterval,teams,wardType,assistants,monsterType,killer,inEnemyJungle,killerTeamID,localgold,globalgold,bountygold,killtype,stageid,killergold,dragontype')
            STORED AS INPUTFORMAT
            'org.apache.hadoop.mapred.TextInputFormat'
            OUTPUTFORMAT
            'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
            LOCATION
            's3://power-rankings-dataset-gprhack/athena-ready/games'
            TBLPROPERTIES (
            'classification'='json',
            'compressionType'='bzip2',
            'typeOfData'='file')
        """,
        ResultConfiguration={"OutputLocation": RESULT_OUTPUT_LOCATION + "/games"}
    )
    return response

# Generate table to record league formats
def generateLeaguesTable():
    response = CLIENT.start_query_execution(
        queryString="""
            CREATE EXTERNAL TABLE lol.`leagues`(
            `id` string, 
            `name` string, 
            `slug` string, 
            `sport` string, 
            `image` string, 
            `lightimage` string, 
            `darkimage` string, 
            `region` string, 
            `priority` int, 
            `displaypriority` struct<position:int,status:string>, 
            `tournaments` array<struct<id:string>>)
            ROW FORMAT SERDE 
            'org.openx.data.jsonserde.JsonSerDe' 
            WITH SERDEPROPERTIES ( 
            'paths'='darkImage,displayPriority,id,image,lightImage,name,priority,region,slug,sport,tournaments') 
            STORED AS INPUTFORMAT 
            'org.apache.hadoop.mapred.TextInputFormat' 
            OUTPUTFORMAT 
            'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
            LOCATION
            's3://power-rankings-dataset-gprhack/athena-ready/leagues'
            TBLPROPERTIES (
            'classification'='json',
            'compressionType'='bzip2', 
            'typeOfData'='file')
        """,
        ResultConfiguration={"OutputLocation": RESULT_OUTPUT_LOCATION + "/leagues"}
    )
    return response

# Generate tables for mapping
def generateTeamMappingsTable():
    response = CLIENT.start_query_execution(
        queryString="""
            CREATE EXTERNAL TABLE lol.`mapping_data`(
            `esportsgameid` string, 
            `platformgameid` string, 
            `teammapping` struct<`200`:string,`100`:string>,
            `participantmapping` struct<`3`:string,`5`:string,`10`:string,`2`:string,`1`:string,`9`:string,`7`:string,`8`:string,`6`:string,`4`:string>)
            ROW FORMAT SERDE 
            'org.openx.data.jsonserde.JsonSerDe' 
            WITH SERDEPROPERTIES ( 
            'paths'='esportsGameId,participantMapping,platformGameId,teamMapping') 
            STORED AS INPUTFORMAT 
            'org.apache.hadoop.mapred.TextInputFormat' 
            OUTPUTFORMAT 
            'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
            LOCATION
            's3://power-rankings-dataset-gprhack/athena-ready/mapping-data'
            TBLPROPERTIES (
            'classification'='json',
            'compressionType'='bzip2', 
            'typeOfData'='file')
        """,
        ResultingConfiguration={"OutputLocation": RESULT_OUTPUT_LOCATION + "/mapping-data"}
    )
    return response

# Generate table for player format
def generatePlayersTable():
    result = CLIENT.start_query_execution(
        queryString="""
            CREATE EXTERNAL TABLE lol.`players`(
            `player_id` string, 
            `handle` string, 
            `first_name` string, 
            `last_name` string, 
            `home_team_id` string)
            ROW FORMAT SERDE 
            'org.openx.data.jsonserde.JsonSerDe' 
            WITH SERDEPROPERTIES ( 
            'paths'='first_name,handle,home_team_id,last_name,player_id') 
            STORED AS INPUTFORMAT 
            'org.apache.hadoop.mapred.TextInputFormat' 
            OUTPUTFORMAT 
            'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
            LOCATION
            's3://power-rankings-dataset-gprhack/athena-ready/players'
            TBLPROPERTIES (
            'classification'='json',
            'compressionType'='bzip2', 
            'typeOfData'='file')
        """,
        ResultConfiguration={"OutputLocation": RESULT_OUTPUT_LOCATION + "/players"}
    )
    return result

# Generate table for team format
def generateTeamsTable():
    result = CLIENT.start_query_execution(
        queryString="""
            CREATE EXTERNAL TABLE lol.`teams`(
            `team_id` string, 
            `name` string, 
            `acronym` string, 
            `slug` string)
            ROW FORMAT SERDE 
            'org.openx.data.jsonserde.JsonSerDe' 
            WITH SERDEPROPERTIES ( 
            'paths'='acronym,name,slug,team_id') 
            STORED AS INPUTFORMAT 
            'org.apache.hadoop.mapred.TextInputFormat' 
            OUTPUTFORMAT 
            'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
            LOCATION
            's3://power-rankings-dataset-gprhack/athena-ready/teams'
            TBLPROPERTIES (
            'classification'='json',
            'compressionType'='bzip2', 
            'typeOfData'='file')
        """,
        ResultConfiguration={"OutputLocation": RESULT_OUTPUT_LOCATION + "/teams"}
    )
    return result

# Generate Table for Tournament format
def generateTournamentsTable():
    result = CLIENT.start_query_execution(
        queryString="""
            CREATE EXTERNAL TABLE lol.`tournaments`(
            `id` string, 
            `leagueid` string, 
            `name` string, 
            `slug` string, 
            `sport` string, 
            `startdate` string, 
            `enddate` string, 
            `stages` array<struct<name:string,type:string,slug:string,sections:array<struct<name:string,matches:array<struct<id:string,type:string,state:string,mode:string,strategy:struct<type:string,count:int>,teams:array<struct<id:string,side:string,record:struct<wins:int,losses:int,ties:int>,result:struct<outcome:string,gamewins:int>,players:array<struct<id:string,role:string>>>>,games:array<struct<id:string,state:string,number:int,teams:array<struct<id:string,side:string,result:struct<outcome:string>>>>>>>,rankings:array<struct<ordinal:int,teams:array<struct<id:string,side:string,record:struct<wins:int,losses:int,ties:int>,result:string,players:array<struct<id:string,role:string>>>>>>>>>>)
            ROW FORMAT SERDE 
            'org.openx.data.jsonserde.JsonSerDe' 
            WITH SERDEPROPERTIES ( 
            'paths'='endDate,id,leagueId,name,slug,sport,stages,startDate') 
            STORED AS INPUTFORMAT 
            'org.apache.hadoop.mapred.TextInputFormat' 
            OUTPUTFORMAT 
            'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
            LOCATION
            's3://power-rankings-dataset-gprhack/athena-ready/tournaments'
            TBLPROPERTIES (
            'classification'='json',
            'compressionType'='bzip2', 
            'typeOfData'='file')
        """,
        ResultConfiguration={"OutputLocation": RESULT_OUTPUT_LOCATION + "/tournaments"}
    )
    return result

def __init__():
    generateGamesTable()