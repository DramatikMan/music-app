import { FC, useEffect } from 'react';
import { Link, NavigateFunction, useNavigate} from 'react-router-dom';
import { Grid, Typography, ButtonGroup, Button } from '@material-ui/core';

import { checkUserInRoom } from './utils';


const HomePage: FC = (): JSX.Element => {
    const navigate: NavigateFunction = useNavigate();

    useEffect(() => { checkUserInRoom(navigate); }, []);

    return (
        <Grid container
            direction='column'
            alignItems='center'
            justifyContent='center'
            style={{ minHeight: '90vh', width: '100%', margin: 0 }}
            spacing={3}
        >
            <Grid item xs={12}>
                <Typography variant='h3'>
                    Music App
                </Typography>
            </Grid>
            <Grid item xs={12}>
                <ButtonGroup disableElevation variant='contained'>
                    <Button color='primary' component={Link} to='/join'>
                        Join a Room
                    </Button>
                    <Button color='default' component={Link} to='/about'>
                        About
                    </Button>
                    <Button color='secondary' component={Link} to='/create'>
                        Create a Room
                    </Button>
                </ButtonGroup>
            </Grid>
        </Grid>
    );
}


export default HomePage;
