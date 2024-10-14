import { type FC } from 'react';
import gameData from '../../game_datas_output.json';

type Props = {
  params: {
    id: number;
  };
};

// TODO: 画面表示を整える
const Page: FC<Props> = (props: Props) => {
  return (
    <>
      <h1>{props.params.id}</h1>
      {gameData.map((game) => (
        <>
          <h1>{game.div}</h1>
          <div>
            <h2>{game.team1}</h2>
            <h2>{game.team2}</h2>
          </div>
        </>
      ))}
    </>
  );
};

export default Page;
