import * as React from 'react'
import { graphql } from 'gatsby'
import "./style.css"
import Logo from "../components/logo"

export const query = graphql`
query {
    allBattingAveragesCsv {
      nodes {
        batting_average
        hits
        hitter_name
        hitter_team
        plate_appearances
        id
      }
    }
    allAverageFastballCsv {
      nodes {
        COL
        SF
        id
      }
    }
    allBonusCsv {
      nodes {
        balls
        inning
        outs
        pitch_release_velocity
        pitch_type
        pitcher_name
        pitcher_team
        strikes
        id
      }
    }
    allExtraBaseHitsCsv {
      nodes {
        XBH
        double
        hitter_name
        hitter_team
        home_run
        single
        triple
        id
      }
    }
    allHardestPitchesCsv {
      nodes {
        pitch_release_velocity
        pitch_type
        pitcher_name
        pitcher_team
        id
      }
    }
    allOpsCsv {
      nodes {
        COL
        SF
        id
      }
    }
  }  
`;

const IndexPage = ({ data }) => {
    const ExtraBaseHits = data.allExtraBaseHitsCsv.nodes;
    const BattingAverages = data.allBattingAveragesCsv.nodes;
    const HardestPitches = data.allHardestPitchesCsv.nodes;
    const AverageFastball = data.allAverageFastballCsv.nodes;
    const Ops = data.allOpsCsv.nodes;
    const Bonus = data.allBonusCsv.nodes;

    return (
        <>
        <Logo />
        <h2>1. Who are the top 10 hitters with the most extra base hits?</h2>
        <table>
            <thead>
                <th>Player Name</th>
                <th>Team</th>
                <th>Extra Base Hits</th>
                <th>Singles</th>
                <th>Doubles</th>
                <th>Triples</th>
                <th>Home Runs</th>
            </thead>
            <tbody>
                {ExtraBaseHits.map(node => (
                    <tr key={node.id}>
                        <td>{node.hitter_name}</td>
                        <td>{node.hitter_team}</td>
                        <td>{node.XBH}</td>
                        <td>{node.single}</td>
                        <td>{node.double}</td>
                        <td>{node.triple}</td>
                        <td>{node.home_run}</td>
                    </tr>
                ))}
            </tbody>
        </table>
        <h2>2. What are the top 10 hardest pitches thrown?</h2>
        <table>
            <thead>
                <th>Player Name</th>
                <th>Team</th>
                <th>Pitch Velocity</th>
                <th>Pitch Type</th>
            </thead>
            <tbody>
                {HardestPitches.map(node => (
                    <tr key={node.id}>
                        <td>{node.pitcher_name}</td>
                        <td>{node.pitcher_team}</td>
                        <td>{node.pitch_release_velocity}</td>
                        <td>{node.pitch_type.replace("_", " ")}</td>
                    </tr>
                ))}
            </tbody>
        </table>
        <h2>3. What is the average four seam fastball velocity for each team's pitchers?</h2>
        <table>
            <thead>
                <th>Rockies Average Velocity</th>
                <th>Giants Average Velocity</th>
            </thead>
            <tbody>
                {AverageFastball.map(node => (
                    <tr key={node.id}>
                        <td>{node.COL}</td>
                        <td>{node.SF}</td>
                    </tr>
                ))}
            </tbody>
        </table>
        <h2>4. Who are the top 5 batting average leaders?</h2>
        <table>
            <thead>
                <tr>
                    <th>Player Name</th>
                    <th>Team</th>
                    <th>Batting Average</th>
                    <th>Hits</th>
                    <th>Plate Appearances</th>
                </tr>
            </thead>
            <tbody>
                {BattingAverages.map(node => (
                    <tr key={node.id}>
                        <td>{node.hitter_name}</td>
                        <td>{node.hitter_team}</td>
                        <td>{node.batting_average}</td>
                        <td>{node.hits}</td>
                        <td>{node.plate_appearances}</td>
                    </tr>
                ))}
            </tbody>
        </table>
        <h2>5. What is the OPS with runners in scoring position for each team?</h2>
        <table>
            <thead>
                <tr>
                    <th>Rockies OPS</th>
                    <th>Giants OPS</th>
                </tr>
            </thead>
            <tbody>
                {Ops.map(node => (
                    <tr key={node.id}>
                        <td>{node.COL}</td>
                        <td>{node.SF}</td>
                    </tr>
                ))}
            </tbody>
        </table>
        <h2>6. Bonus: List all the pitches thrown that have the exact same velocity.</h2>
        <table>
            <thead>
                <tr>
                    <th>Player Name</th>
                    <th>Team</th>
                    <th>Pitch Velocity</th>
                    <th>Pitch Type</th>
                    <th>Inning</th>
                    <th>Balls</th>
                    <th>Strikes</th>
                    <th>Outs</th>
                </tr>
            </thead>
            <tbody>
                {Bonus.map(node => (
                    <tr key={node.id}>
                        <td>{node.pitcher_name}</td>
                        <td>{node.pitcher_team}</td>
                        <td>{node.pitch_release_velocity}</td>
                        <td>{node.pitch_type.replace("_", " ")}</td>
                        <td>{node.inning}</td>
                        <td>{node.balls}</td>
                        <td>{node.strikes}</td>
                        <td>{node.outs}</td>
                    </tr>
                ))}
            </tbody>
        </table>
        <p>
        The Big-O runtime to find pitches of the same velocity is O(n), where n is the number of pitches in play_by_play.json:
        </p>
        <ol>
            <li>Iterate through all pitches, grouping by pitch velocity - O(n)</li>
            <li>Select pitch velocities that occur more than once - O(n)</li>
            <li>Iterate through all pitches, selecting pitch velocities found in step 2 - O(n)*</li>
        </ol>
        <p>
        *Assuming pandas stores keys in a hashmap with O(1) lookup. If pandas stores keys in a list with O(m) lookup, where m is the same velocity pitches, the overall runtime would be O(n*m).
        </p>
        </>
    )
}

export default IndexPage