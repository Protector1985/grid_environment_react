import { setDirection } from "./redux/slices/playerSlice";

export function makeMove(direction: string, currentPosition: number, dispatch:any) {

    function hitWall() {
        const rightWallPositions = [8, 17, 26, 35, 44];
        const leftWallPositions = [0, 9, 18, 27, 36];

        switch (direction) {
            case "RIGHT":
                dispatch(setDirection(`RIGHT_${Math.random()}`))
                return rightWallPositions.includes(currentPosition);
            case "LEFT":
                dispatch(setDirection(`LEFT_${Math.random()}`))
                return leftWallPositions.includes(currentPosition );
            case "UP":
                dispatch(setDirection(`UP_${Math.random()}`))
                return currentPosition - 10 < 0;
            case "DOWN":
                dispatch(setDirection(`DOWN_${Math.random()}`))
                return currentPosition + 10 > 45;
            default:
                return false;
        }
    }

    switch (direction) {
        case "LEFT":
            return !hitWall() ? currentPosition - 1 : `WALL${Math.random()}`;
        case "RIGHT":
            return !hitWall() ? currentPosition + 1 : `WALL${Math.random()}`;
        case "UP":
            return !hitWall() ? currentPosition - 9 : `WALL${Math.random()}`;
        case "DOWN":
            return !hitWall() ? currentPosition + 9 : `WALL${Math.random()}`;
       
        default:
            return currentPosition;
    }
}


export function sanitizeDirectionString(inputString:string) {
    const directions = ["LEFT", "RIGHT", "UP", "DOWN"];

    // Find the direction in the input string
    const foundDirection = directions.find(direction => inputString.includes(direction));

    return foundDirection || "Invalid Direction"; // Return the found direction or a default value
}