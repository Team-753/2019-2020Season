package org.frcteam2910.c2019.commands;

import edu.wpi.first.wpilibj.command.Command;
import org.frcteam2910.c2019.Robot;
import org.frcteam753.c2020.subsystems.DrivetrainSubsystem;
import org.frcteam753.common.math.Rotation2;
import org.frcteam753.common.math.Vector2;

public class HolonomicDriveCommand extends Command {
    public HolonomicDriveCommand() {
        requires(DrivetrainSubsystem.getInstance());
    }

    @Override
    protected void execute() {

        double forward = Robot.getOi().myOnlyJoy.getX​();
        double strafe = Robot.getOi().myOnlyJoy.getY​();
        double rotation = Robot.getOi().myOnlyJoy.getZ();

        boolean robotOriented = true;
        boolean reverseRobotOriented = false;

        Vector2 translation = new Vector2(forward, strafe);

        if (reverseRobotOriented) {
            robotOriented = true;
            translation = translation.rotateBy(Rotation2.fromDegrees(180.0));
        }

        DrivetrainSubsystem.getInstance().holonomicDrive(translation, rotation, !robotOriented);
    }

    @Override
    protected boolean isFinished() {
        return false;
    }
}
