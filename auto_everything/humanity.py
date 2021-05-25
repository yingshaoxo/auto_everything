import pandas as pd
import os


class Friendship():
    def __init__(self, csv_path=None):
        if csv_path == None:
            self.__df_path = os.path.join(os.getcwd(), 'friendships.csv')
        else:
            self.__df_path = os.path.abspath(csv_path)

        if not os.path.exists(self.__df_path):
            self.df = pd.DataFrame(columns=[
                'name',
                'description',
                'positive_power',
                'negative_power',
                'balanced_times'
            ])
        else:
            self.df = pd.read_csv(self.__df_path)

    def __str__(self):
        return '-' * 30 + '\n' + str(self.df.head())

    def add_person(self, name):
        temp_df = self.df.loc[self.df['name'] == name]
        if len(temp_df) >= 1:
            print('You already have it')
        else:
            self.df = self.df.append(
                {
                    'name': name,
                    'description': '',
                    'positive_power': 0,
                    'negative_power': 0,
                    'balanced_times': 0,
                },
                ignore_index=True
            )

    def delete_person(self, name):
        self.df = self.df[self.df['name'] != name]

    def giving(self, name, power):
        temp_df = self.df.loc[self.df['name'] == name]
        if len(temp_df) >= 1:
            new_value = temp_df.iloc[0]['positive_power'] + power
            temp_df.loc[:, 'positive_power'] = new_value
            temp_df = self.__calculate_balanced_times(temp_df)
            self.df.update(temp_df)
        else:
            print(f"{name} does not exist in your friendship list!")

    def taking(self, name, power):
        temp_df = self.df.loc[self.df['name'] == name]
        if len(temp_df) >= 1:
            new_value = temp_df.iloc[0]['negative_power'] + power
            temp_df.loc[:, 'negative_power'] = new_value
            temp_df = self.__calculate_balanced_times(temp_df)
            self.df.update(temp_df)
        else:
            print(f"{name} does not exist in your friendship list!")

    def __calculate_balanced_times(self, single_row_df):
        positive = single_row_df.iloc[0]['positive_power']
        negative = single_row_df.iloc[0]['negative_power']
        balanced_times = single_row_df.iloc[0]['balanced_times']
        if positive == negative:
            single_row_df.loc[:, 'balanced_times'] = balanced_times + 1
        return single_row_df

    def seek_for_help(self, description=''):
        temp_df = self.df.loc[self.df['positive_power'] > self.df['negative_power']]
        temp_df['released_power'] = temp_df['positive_power'] - temp_df['negative_power']
        sorted_df = temp_df.sort_values(['released_power', 'balanced_times'])
        print(sorted_df.head())

    def can_i_help(self, name=None):
        temp_df = self.df.loc[self.df['negative_power'] > self.df['positive_power']]
        temp_df['borrowed_power'] = temp_df['negative_power'] - temp_df['positive_power']
        sorted_df = temp_df.sort_values(['borrowed_power', 'balanced_times'])
        print(sorted_df.head())

    def commit(self):
        self.df.to_csv(self.__df_path, index=False)


if __name__ == "__main__":
    print('\n' * 50)
    friendship = Friendship('/home/yingshaoxo/Documents/friendship.csv')
    friendship.add_person('A')
    friendship.add_person('B')
    friendship.giving('A', 5)
    friendship.taking('B', 3)
    friendship.seek_for_help()
    friendship.can_i_help()
    # friendship.commit()
