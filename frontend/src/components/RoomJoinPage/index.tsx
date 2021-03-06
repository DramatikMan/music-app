import { Button, Grid, TextField, Typography } from '@material-ui/core';
import { FC, Dispatch } from 'react';
import { Link, NavigateFunction, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';

import State from '../../types/state';
import { RoomJoinPageActions } from '../../types/actions/RoomJoinPage';
import { setRoomCode } from '../../actionCreators/RoomJoinPage';
import { enterRoomPressed } from './utils';


const RoomJoinPage: FC = (): JSX.Element => {
    const dispatch: Dispatch<RoomJoinPageActions> = useDispatch();
    const navigate: NavigateFunction = useNavigate();

    const roomCode: string = useSelector(
        (state: State): string => state.RoomJoinPage.roomCode
    );
    const helperText: string = useSelector(
        (state: State): string => state.RoomJoinPage.helperText
    );

    return (
        <Grid container
            direction='column'
            alignItems='center'
            justifyContent='center'
            style={{ minHeight: '90vh', width: '100%', margin: 0 }}
            spacing={1}
        >
            <Grid item xs={12}>
                <Typography variant='h4'>
                    Join a Room
                </Typography>
            </Grid>
            <Grid item xs={12}>
                <TextField
                    label='Code'
                    placeholder='Enter Room code'
                    error={Boolean(helperText)}
                    helperText={helperText}
                    variant='outlined'
                    onChange={ e => dispatch(setRoomCode(e.target.value)) }
                />
            </Grid>
            <Grid item xs={12}>
                <Button
                    variant='contained'
                    color='primary'
                    onClick={ () => enterRoomPressed(
                        roomCode,
                        navigate,
                        dispatch)
                    }
                >
                    Enter Room
                </Button>
            </Grid>
            <Grid item xs={12}>
                <Button
                    variant='contained'
                    color='secondary'
                    component={Link}
                    to='/'
                >
                    Back
                </Button>
            </Grid>
        </Grid>
    );
}


export default RoomJoinPage;
